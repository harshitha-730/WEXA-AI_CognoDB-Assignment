import os
import time
import random
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

from benchmark.cognodb import CognoDBBenchmark


DATASET = "datasets/Wiki-Vote.txt"
CLIENT_COUNTS = [1, 4, 8]
OPERATIONS_PER_CLIENT = 20


def run_client(db, node_ids, operations):
    completed = 0
    failed = 0

    for _ in range(operations):
        try:
            user_id = random.choice(node_ids)

            operation = random.choice([
                "lookup",
                "traversal",
                "aggregation",
                "write"
            ])

            if operation == "lookup":
                db.lookup_user(user_id)

            elif operation == "traversal":
                db.traverse(user_id)

            elif operation == "aggregation":
                db.aggregation()

            elif operation == "write":
                target = random.choice(node_ids)

                db.execute_query(
                    """
                    MERGE (u1:User {id: $source})
                    MERGE (u2:User {id: $target})
                    MERGE (u1)-[:VOTED_FOR]->(u2)
                    """,
                    {
                        "source": user_id,
                        "target": target
                    }
                )

            completed += 1

        except Exception:
            failed += 1

    return completed, failed


def main():

    db = CognoDBBenchmark()
    db.connect()

    try:

        print("\nLoading node IDs...")

        rows = db.execute_query(
            """
            MATCH (n:User)
            RETURN n.id AS id
            LIMIT 5000
            """
        )

        node_ids = [row["id"] for row in rows]

        if not node_ids:
            raise RuntimeError("No nodes found in CognoDB.")

        print(f"Using {len(node_ids)} nodes")

        results = []

        # Warm-up
        print("\n🔥 Running warm-up...")

        db.lookup_user(node_ids[0])
        db.traverse(node_ids[0])
        db.aggregation()

        print("Warm-up completed")

        for clients in CLIENT_COUNTS:

            total_operations = clients * OPERATIONS_PER_CLIENT

            print(
                f"\nRunning mixed workload: "
                f"{clients} clients / "
                f"{total_operations} operations"
            )

            start = time.perf_counter()

            completed = 0
            failed = 0

            with ThreadPoolExecutor(
                max_workers=clients
            ) as executor:

                futures = [
                    executor.submit(
                        run_client,
                        db,
                        node_ids,
                        OPERATIONS_PER_CLIENT
                    )
                    for _ in range(clients)
                ]

                for future in as_completed(futures):

                    success, errors = future.result()

                    completed += success
                    failed += errors

            elapsed = time.perf_counter() - start

            throughput = (
                completed / elapsed
                if elapsed > 0
                else 0
            )

            print(
                f"Clients: {clients} | "
                f"Completed: {completed} | "
                f"Failed: {failed} | "
                f"Time: {elapsed:.3f}s | "
                f"Throughput: {throughput:.2f} ops/sec"
            )

            results.append({
                "platform": "CognoDB",
                "clients": clients,
                "operations": total_operations,
                "completed": completed,
                "failed": failed,
                "duration_s": round(elapsed, 3),
                "throughput_ops_s": round(throughput, 2)
            })

        # Save CSV
        os.makedirs("results", exist_ok=True)

        output = "results/cognodb_mixed_workload.csv"

        with open(output, "w", encoding="utf-8") as f:

            f.write(
                "platform,clients,operations,"
                "completed,failed,duration_s,"
                "throughput_ops_s\n"
            )

            for row in results:

                f.write(
                    f"{row['platform']},"
                    f"{row['clients']},"
                    f"{row['operations']},"
                    f"{row['completed']},"
                    f"{row['failed']},"
                    f"{row['duration_s']},"
                    f"{row['throughput_ops_s']}\n"
                )

        print(f"\n✅ Results saved to {output}")

    finally:
        db.close()


if __name__ == "__main__":
    main()