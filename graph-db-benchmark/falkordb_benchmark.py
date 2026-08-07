import csv, os
from dotenv import load_dotenv
from benchmark.falkordb import FalkorDBBenchmark

load_dotenv()

db = FalkorDBBenchmark(
    host=os.getenv("FALKORDB_HOST"),
    port=int(os.getenv("FALKORDB_PORT")),
)

results = {
    "platform": "FalkorDB",
    "node_count": db.count_nodes(),
    "rel_count": db.count_relationships(),
}
db.node_ids = [r[0] for r in db.execute_query("MATCH (n:User) RETURN n.id LIMIT 5000")]

for hops in (1, 2, 3):
    p50, p95 = db.bench_traversal(hops)
    results[f"traversal_{hops}hop_p50_ms"], results[f"traversal_{hops}hop_p95_ms"] = p50, p95

results["point_lookup_p50_ms"], results["point_lookup_p95_ms"] = db.bench_point_lookup()
results["filtered_lookup_p50_ms"], results["filtered_lookup_p95_ms"] = db.bench_filtered_lookup()
results["aggregation_p50_ms"], results["aggregation_p95_ms"] = db.bench_aggregation()
results.update(db.footprint())

os.makedirs("results", exist_ok=True)
with open("results/falkordb_results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=results.keys())
    w.writeheader()
    w.writerow(results)

print(results)
print("Saved results/falkordb_results.csv")