import csv
import os

RESULTS_DIR = "results"

FILES = {
    "CognoDB": "cognodb_results.csv",
    "Neo4j": "neo4j_results.csv",
    "Memgraph": "memgraph_results.csv",
    "FalkorDB": "falkordb_results.csv",
    "Kuzu": "kuzu_results.csv",
}


def load_result(platform, filename):
    path = os.path.join(RESULTS_DIR, filename)

    if not os.path.exists(path):
        print(f"⚠️ Missing result: {path}")
        return None

    with open(path, newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print(f"⚠️ Empty result: {path}")
        return None

    row = rows[0]
    row["platform"] = platform

    return row


results = []

for platform, filename in FILES.items():
    result = load_result(platform, filename)

    if result:
        results.append(result)


if not results:
    raise RuntimeError("No benchmark results found.")


# --------------------------------------------------
# Comparison output
# --------------------------------------------------

fields = [
    "platform",

    "node_count",
    "rel_count",

    "traversal_1hop_p50_ms",
    "traversal_1hop_p95_ms",

    "traversal_2hop_p50_ms",
    "traversal_2hop_p95_ms",

    "traversal_3hop_p50_ms",
    "traversal_3hop_p95_ms",

    "point_lookup_p50_ms",
    "point_lookup_p95_ms",

    "filtered_lookup_p50_ms",
    "filtered_lookup_p95_ms",

    "aggregation_p50_ms",
    "aggregation_p95_ms",
]


output_file = os.path.join(
    RESULTS_DIR,
    "comparison.csv"
)


with open(output_file, "w", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fields,
        extrasaction="ignore"
    )

    writer.writeheader()

    for result in results:
        writer.writerow(result)


# --------------------------------------------------
# Print readable comparison
# --------------------------------------------------

print("\n================ BENCHMARK COMPARISON ================\n")

for result in results:

    print(f"Platform: {result['platform']}")

    print(
        f"  1-hop traversal: "
        f"p50={result.get('traversal_1hop_p50_ms', 'N/A')} ms | "
        f"p95={result.get('traversal_1hop_p95_ms', 'N/A')} ms"
    )

    print(
        f"  2-hop traversal: "
        f"p50={result.get('traversal_2hop_p50_ms', 'N/A')} ms | "
        f"p95={result.get('traversal_2hop_p95_ms', 'N/A')} ms"
    )

    print(
        f"  3-hop traversal: "
        f"p50={result.get('traversal_3hop_p50_ms', 'N/A')} ms | "
        f"p95={result.get('traversal_3hop_p95_ms', 'N/A')} ms"
    )

    print(
        f"  Point lookup: "
        f"p50={result.get('point_lookup_p50_ms', 'N/A')} ms | "
        f"p95={result.get('point_lookup_p95_ms', 'N/A')} ms"
    )

    print(
        f"  Filtered lookup: "
        f"p50={result.get('filtered_lookup_p50_ms', 'N/A')} ms | "
        f"p95={result.get('filtered_lookup_p95_ms', 'N/A')} ms"
    )

    print(
        f"  Aggregation: "
        f"p50={result.get('aggregation_p50_ms', 'N/A')} ms | "
        f"p95={result.get('aggregation_p95_ms', 'N/A')} ms"
    )

    print()


print(f"Comparison saved to: {output_file}")