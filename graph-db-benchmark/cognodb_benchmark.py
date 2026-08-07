import csv
import os
import random
import statistics
import time

from dotenv import load_dotenv
from benchmark.cognodb import CognoDBBenchmark

load_dotenv()

RUNS = 100
WARMUP = 10

db = CognoDBBenchmark()
db.connect()


def measure(function, runs=RUNS, warmup=WARMUP):
    # Warm-up runs
    for _ in range(warmup):
        function()

    times = []

    for _ in range(runs):
        start = time.perf_counter()
        function()
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

    times.sort()

    p50 = statistics.median(times)
    p95 = times[int(len(times) * 0.95) - 1]

    return round(p50, 3), round(p95, 3)


# --------------------------------------------------
# Basic graph counts
# --------------------------------------------------

node_count = db.count_nodes()
rel_count = db.count_relationships()

print(f"Nodes: {node_count}")
print(f"Relationships: {rel_count}")


# --------------------------------------------------
# Get user IDs
# --------------------------------------------------

users = db.execute_query(
    """
    MATCH (u:User)
    RETURN u.id AS id
    LIMIT 5000
    """
)

user_ids = [row["id"] for row in users]

if not user_ids:
    raise RuntimeError("No users found in CognoDB.")


# --------------------------------------------------
# Results
# --------------------------------------------------

results = {
    "platform": "CognoDB",
    "node_count": node_count,
    "rel_count": rel_count,
}


# --------------------------------------------------
# Traversal: 1-hop, 2-hop, 3-hop
# --------------------------------------------------

def traversal(hops):

    pattern = "-[:VOTED_FOR]->()" * hops

    def run():
        uid = random.choice(user_ids)

        db.execute_query(
            f"""
            MATCH (u:User {{id: $id}}){pattern}
            RETURN count(*)
            """,
            {"id": uid}
        )

    return measure(run)


for hop in [1, 2, 3]:

    p50, p95 = traversal(hop)

    results[f"traversal_{hop}hop_p50_ms"] = p50
    results[f"traversal_{hop}hop_p95_ms"] = p95

    print(
        f"{hop}-hop Traversal: "
        f"p50={p50} ms, p95={p95} ms"
    )


# --------------------------------------------------
# Point lookup
# --------------------------------------------------

def point_lookup():

    uid = random.choice(user_ids)

    db.lookup_user(uid)


p50, p95 = measure(point_lookup)

results["point_lookup_p50_ms"] = p50
results["point_lookup_p95_ms"] = p95

print(
    f"Point Lookup: "
    f"p50={p50} ms, p95={p95} ms"
)


# --------------------------------------------------
# Filtered lookup
# --------------------------------------------------

def filtered_lookup():

    uid = random.choice(user_ids)

    db.execute_query(
        """
        MATCH (u:User)
        WHERE u.id = $id
        RETURN u
        """,
        {"id": uid}
    )


p50, p95 = measure(filtered_lookup)

results["filtered_lookup_p50_ms"] = p50
results["filtered_lookup_p95_ms"] = p95

print(
    f"Filtered Lookup: "
    f"p50={p50} ms, p95={p95} ms"
)


# --------------------------------------------------
# Aggregation
# --------------------------------------------------

p50, p95 = measure(db.aggregation)

results["aggregation_p50_ms"] = p50
results["aggregation_p95_ms"] = p95

print(
    f"Aggregation: "
    f"p50={p50} ms, p95={p95} ms"
)


# --------------------------------------------------
# Save results
# --------------------------------------------------

os.makedirs("results", exist_ok=True)

output_file = "results/cognodb_results.csv"

with open(output_file, "w", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results.keys()
    )

    writer.writeheader()
    writer.writerow(results)


print("\nCognoDB Benchmark Results:")
print(results)

print(f"\nSaved: {output_file}")

db.close()