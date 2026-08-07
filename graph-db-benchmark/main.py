from benchmark.cognodb import CognoDBBenchmark
from utils.benchmark import measure_execution_time
from utils.metrics import save_metrics

db = CognoDBBenchmark()
db.connect()

results = []

# Lookup Benchmark
_, lookup_time = measure_execution_time(db.lookup_user, 30)
print(f"Lookup Time: {lookup_time:.3f} ms")
results.append(("Lookup", lookup_time))

# Traversal Benchmark
_, traversal_time = measure_execution_time(db.traverse, 30)
print(f"Traversal Time: {traversal_time:.3f} ms")
results.append(("Traversal", traversal_time))

# Aggregation Benchmark
top_users, aggregation_time = measure_execution_time(db.aggregation)
print(f"Aggregation Time: {aggregation_time:.3f} ms")
results.append(("Aggregation", aggregation_time))

print("\nTop 10 Users by Outgoing Votes")
for row in top_users:
    print(f"User {row['user_id']} -> {row['votes']} votes")

# Save benchmark results
save_metrics(results)

db.close()

print("\nBenchmark results saved to results/benchmark_results.csv")