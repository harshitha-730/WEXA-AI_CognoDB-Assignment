import csv
import os

from benchmark.kuzu import KuzuBenchmark


db = KuzuBenchmark("kuzu_db")

db.connect()

try:

    results = {
        "platform": "Kùzu",
        "node_count": db.count_nodes(),
        "rel_count": db.count_relationships(),
    }

    # -------------------------
    # Load node IDs
    # -------------------------

    print("\nLoading node IDs...")

    db.load_node_ids(5000)

    print(f"Using {len(db.node_ids)} nodes")

    # -------------------------
    # Warm-up
    # -------------------------

    print("\n🔥 Running warm-up...")

    WARMUP_RUNS = 10

    import random

    for _ in range(WARMUP_RUNS):

        uid = random.choice(db.node_ids)

        db.lookup_user(uid)

        db.execute_query(
            f"""
            MATCH (u:User {{id:{uid}}})
            -[:VOTED_FOR]->()
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

        print(
            f"\nRunning {hops}-hop traversal..."
        )

        p50, p95 = db.bench_traversal(hops)

        results[
            f"traversal_{hops}hop_p50_ms"
        ] = p50

        results[
            f"traversal_{hops}hop_p95_ms"
        ] = p95

    # -------------------------
    # Point lookup
    # -------------------------

    print("\nRunning point lookup...")

    p50, p95 = db.bench_point_lookup()

    results["point_lookup_p50_ms"] = p50
    results["point_lookup_p95_ms"] = p95

    # -------------------------
    # Filtered lookup
    # -------------------------

    print("Running filtered lookup...")

    p50, p95 = db.bench_filtered_lookup()

    results["filtered_lookup_p50_ms"] = p50
    results["filtered_lookup_p95_ms"] = p95

    # -------------------------
    # Aggregation
    # -------------------------

    print("Running aggregation...")

    p50, p95 = db.bench_aggregation()

    results["aggregation_p50_ms"] = p50
    results["aggregation_p95_ms"] = p95

    # -------------------------
    # Footprint
    # -------------------------

    results.update(
        db.footprint("kuzu_db")
    )

    # -------------------------
    # Save
    # -------------------------

    os.makedirs(
        "results",
        exist_ok=True
    )

    with open(
        "results/kuzu_results.csv",
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
    # Print
    # -------------------------

    print(
        "\n=============================="
    )

    print(
        "Kùzu Benchmark Results"
    )

    print(
        "=============================="
    )

    for key, value in results.items():
        print(f"{key}: {value}")

    print(
        "\nSaved: results/kuzu_results.csv"
    )

finally:

    db.close()