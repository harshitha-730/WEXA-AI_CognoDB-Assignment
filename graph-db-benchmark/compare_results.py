import csv
import os


RESULT_FILES = {
    "CognoDB": "results/cognodb_results.csv",
    "Neo4j": "results/neo4j_results.csv",
    "Memgraph": "results/memgraph_results.csv",
    "FalkorDB": "results/falkordb_results.csv",
    "Kùzu": "results/kuzu_results.csv",
}


OUTPUT_FILE = "results/final_comparison.csv"


FIELDS = [
    "Database",
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

    "used_memory_human",
    "used_memory_bytes",

    "on_disk_size_bytes",
    "on_disk_size_human",

    "note",
]


def read_result(path):
    """
    Read benchmark CSV using Latin-1 encoding.
    Latin-1 handles characters such as ù in Kùzu
    without UnicodeDecodeError.
    """

    with open(
        path,
        "r",
        encoding="latin-1",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        try:
            return next(reader)
        except StopIteration:
            raise ValueError(f"Empty result file: {path}")


def clean_value(row, field):
    value = row.get(field, "")

    if value is None:
        return ""

    return value


os.makedirs("results", exist_ok=True)

all_results = []


print("\n================ BENCHMARK COMPARISON ================\n")


for database, path in RESULT_FILES.items():

    if not os.path.exists(path):
        print(f"WARNING: Missing {path}")
        continue

    row = read_result(path)

    result = {
        "Database": database
    }

    for field in FIELDS:

        if field != "Database":
            result[field] = clean_value(row, field)

    all_results.append(result)


    print(f"Platform: {database}")

    print(
        f"1-hop traversal: "
        f"p50={result['traversal_1hop_p50_ms']} ms | "
        f"p95={result['traversal_1hop_p95_ms']} ms"
    )

    print(
        f"2-hop traversal: "
        f"p50={result['traversal_2hop_p50_ms']} ms | "
        f"p95={result['traversal_2hop_p95_ms']} ms"
    )

    print(
        f"3-hop traversal: "
        f"p50={result['traversal_3hop_p50_ms']} ms | "
        f"p95={result['traversal_3hop_p95_ms']} ms"
    )

    print(
        f"Point lookup: "
        f"p50={result['point_lookup_p50_ms']} ms | "
        f"p95={result['point_lookup_p95_ms']} ms"
    )

    print(
        f"Filtered lookup: "
        f"p50={result['filtered_lookup_p50_ms']} ms | "
        f"p95={result['filtered_lookup_p95_ms']} ms"
    )

    print(
        f"Aggregation: "
        f"p50={result['aggregation_p50_ms']} ms | "
        f"p95={result['aggregation_p95_ms']} ms"
    )

    print()


# -------------------------------------------------------
# Write final comparison
# -------------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="latin-1",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=FIELDS
    )

    writer.writeheader()
    writer.writerows(all_results)


print(
    f"Final comparison saved to: {OUTPUT_FILE}"
)