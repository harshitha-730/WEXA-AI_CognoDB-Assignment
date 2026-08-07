import csv
import os
import random
import statistics
import time

from dotenv import load_dotenv
from benchmark.falkordb import FalkorDBBenchmark

load_dotenv()

db = FalkorDBBenchmark(
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=int(os.getenv("FALKORDB_PORT", "6379")),
)

db.connect()

try:
    # -------------------------
    # Basic counts
    # -------------------------

    results = {
        "platform": "FalkorDB",
        "node_count": db.count_nodes(),
        "rel_count": db.count_relationships(),
    }

    # -------------------------
    # Load node IDs
    # -------------------------

    print("\nLoading node IDs...")

    rows = db.execute_query(
        "MATCH (n:User) RETURN n.id LIMIT 5000"
    )

    db.node_ids = [row[0] for row in rows]

    print(f"Using {len(db.node_ids)} nodes")

    # -------------------------
    # Benchmark functions
    # -------------------------

    def measure(fn, runs=100):
        latencies = []

        for _ in range(runs):
            start = time.perf_counter()
            fn()
            elapsed = (time.perf_counter() - start) * 1000
            latencies.append(elapsed)

        latencies.sort()

        p50 = statistics.median(latencies)
        p95_index = max(0, int(len(latencies) * 0.95) - 1)
        p95 = latencies[p95_index]

        return round(p50, 3), round(p95, 3)

    def traversal(hops):
        pattern = "-[:VOTED_FOR]->()" * hops

        def run():
            uid = random.choice(db.node_ids)

            db.execute_query(
                f"""
                MATCH (u:User {{id:{uid}}}){pattern}
                RETURN count(*)
                """
            )

        return measure(run)

    def point_lookup():
        def run():
            uid = random.choice(db.node_ids)
            db.lookup_user(uid)

        return measure(run)

    def filtered_lookup():
        def run():
            uid = random.choice(db.node_ids)

            db.execute_query(
                f"""
                MATCH (u:User)
                WHERE u.id = {uid}
                RETURN u
                """
            )

        return measure(run)

    # -------------------------
    # Warm-up
    # -------------------------

    print("\n🔥 Running warm-up...")

    WARMUP_RUNS = 10

    for _ in range(WARMUP_RUNS):
        uid = random.choice(db.node_ids)

        db.lookup_user(uid)

        db.execute_query(
            f"""
            MATCH (u:User {{id:{uid}}})-[:VOTED_FOR]->()
            RETURN count(*)
            """
        )

        db.execute_query(
            f"""
            MATCH (u:User)
            WHERE u.id = {uid}
            RETURN u
            """
        )

        db.aggregation()

    print("Warm-up completed")

    # -------------------------
    # Traversals
    # -------------------------

    for hops in (1, 2, 3):

        print(f"\nRunning {hops}-hop traversal...")

        p50, p95 = traversal(hops)

        results[f"traversal_{hops}hop_p50_ms"] = p50
        results[f"traversal_{hops}hop_p95_ms"] = p95

    # -------------------------
    # Point lookup
    # -------------------------

    print("\nRunning point lookup...")

    p50, p95 = point_lookup()

    results["point_lookup_p50_ms"] = p50
    results["point_lookup_p95_ms"] = p95

    # -------------------------
    # Filtered lookup
    # -------------------------

    print("Running filtered lookup...")

    p50, p95 = filtered_lookup()

    results["filtered_lookup_p50_ms"] = p50
    results["filtered_lookup_p95_ms"] = p95

    # -------------------------
    # Aggregation
    # -------------------------

    print("Running aggregation...")

    p50, p95 = measure(db.aggregation)

    results["aggregation_p50_ms"] = p50
    results["aggregation_p95_ms"] = p95

    # -------------------------
    # Memory footprint
    # -------------------------

    try:
        results.update(db.footprint())
    except Exception:
        results["used_memory_human"] = "N/A"
        results["used_memory_bytes"] = "N/A"

    # -------------------------
    # Save results
    # -------------------------

    os.makedirs("results", exist_ok=True)

    with open(
        "results/falkordb_results.csv",
        "w",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=results.keys()
        )

        writer.writeheader()
        writer.writerow(results)

    # -------------------------
    # Print results
    # -------------------------

    print("\n==============================")
    print("FalkorDB Benchmark Results")
    print("==============================")

    for key, value in results.items():
        print(f"{key}: {value}")

    print("\nSaved: results/falkordb_results.csv")

finally:
    db.close()