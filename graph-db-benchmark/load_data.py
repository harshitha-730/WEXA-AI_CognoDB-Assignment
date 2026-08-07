import time
import csv
import os

from benchmark.cognodb import CognoDBBenchmark
from utils.loader import load_wiki_vote


DATASET = "datasets/Wiki-Vote.txt"
BATCH_SIZE = 1000


def main():
    db = CognoDBBenchmark()
    db.connect()

    try:
        # Load dataset
        edges = load_wiki_vote(DATASET)

        print(f"Loaded {len(edges)} relationships")
        print(f"Batch size: {BATCH_SIZE}")

        # Clear existing graph
        print("Clearing existing CognoDB graph...")

        db.execute_query(
            """
            MATCH (n:User)
            DETACH DELETE n
            """
        )

        # Start ingestion timer
        start = time.perf_counter()

        total = len(edges)

        # Insert in batches
        for i in range(0, total, BATCH_SIZE):
            batch = edges[i:i + BATCH_SIZE]

            db.insert_edges(batch)

            inserted = min(i + BATCH_SIZE, total)

            print(
                f"Inserted {inserted} / {total}",
                end="\r"
            )

        # Stop timer
        elapsed = time.perf_counter() - start

        throughput = total / elapsed

        print()
        print(f"Insertion Time: {elapsed:.3f} seconds")
        print(
            f"Ingestion Throughput: "
            f"{throughput:.2f} relationships/sec"
        )

        # Verify database
        nodes = db.count_nodes()
        relationships = db.count_relationships()

        print(f"Nodes: {nodes}")
        print(f"Relationships: {relationships}")

        # Save ingestion results
        os.makedirs("results", exist_ok=True)

        output_file = "results/cognodb_ingestion.csv"

        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "platform",
                "node_count",
                "rel_count",
                "batch_size",
                "insertion_time_s",
                "ingestion_throughput_rel_s"
            ])

            writer.writerow([
                "CognoDB",
                nodes,
                relationships,
                BATCH_SIZE,
                round(elapsed, 3),
                round(throughput, 2)
            ])

        print(
            f"Ingestion results saved to {output_file}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()