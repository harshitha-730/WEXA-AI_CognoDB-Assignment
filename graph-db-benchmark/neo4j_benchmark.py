import csv
import os
import time
import random
import statistics

from dotenv import load_dotenv
from benchmark.neo4j import Neo4jBenchmark

load_dotenv()


db = Neo4jBenchmark(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD")
)

db.connect()


def measure(fn, runs=100):
    times = []

    for _ in range(runs):
        start = time.perf_counter()
        fn()
        times.append((time.perf_counter() - start) * 1000)

    times.sort()

    p50 = statistics.median(times)
    p95 = times[int(len(times) * 0.95) - 1]

    return round(p50, 3), round(p95, 3)


# -------------------------
# Basic counts
# -------------------------

results = {
    "platform": "Neo4j",
    "node_count": db.count_nodes(),
    "rel_count": db.count_relationships()
}


# Get random user IDs

users = db.execute_query(
    """
    MATCH (u:User)
    RETURN u.id AS id
    LIMIT 5000
    """
)

user_ids = [u["id"] for u in users]


# -------------------------
# Traversal benchmark
# -------------------------

def traversal(hops):

    pattern = "-[:VOTED_FOR]->()" * hops

    def run():
        uid = random.choice(user_ids)

        db.execute_query(
            f"""
            MATCH (u:User {{id:$id}}){pattern}
            RETURN count(*)
            """,
            {"id": uid}
        )

    return measure(run)


for hop in [1,2,3]:

    p50, p95 = traversal(hop)

    results[f"traversal_{hop}hop_p50_ms"] = p50
    results[f"traversal_{hop}hop_p95_ms"] = p95



# -------------------------
# Point lookup
# -------------------------

def lookup():

    uid = random.choice(user_ids)

    db.lookup_user(uid)


p50,p95 = measure(lookup)

results["point_lookup_p50_ms"] = p50
results["point_lookup_p95_ms"] = p95



# -------------------------
# Filter lookup
# -------------------------

def filtered():

    uid=random.choice(user_ids)

    db.execute_query(
        """
        MATCH (u:User)
        WHERE u.id=$id
        RETURN u
        """,
        {"id":uid}
    )


p50,p95 = measure(filtered)

results["filtered_lookup_p50_ms"]=p50
results["filtered_lookup_p95_ms"]=p95



# -------------------------
# Aggregation
# -------------------------

p50,p95 = measure(db.aggregation)

results["aggregation_p50_ms"]=p50
results["aggregation_p95_ms"]=p95



# -------------------------
# Save
# -------------------------

os.makedirs("results",exist_ok=True)

with open(
    "results/neo4j_results.csv",
    "w",
    newline=""
) as f:

    writer=csv.DictWriter(
        f,
        fieldnames=results.keys()
    )

    writer.writeheader()
    writer.writerow(results)


print(results)

print(
    "Saved results/neo4j_results.csv"
)


db.close()