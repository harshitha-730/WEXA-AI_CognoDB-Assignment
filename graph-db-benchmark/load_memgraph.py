from dotenv import load_dotenv
import csv
import os
import time

from benchmark.memgraph import MemgraphBenchmark
from utils.loader import load_wiki_vote

load_dotenv()

db = MemgraphBenchmark(
    os.getenv("MEMGRAPH_URI"),
    os.getenv("MEMGRAPH_USERNAME"),
    os.getenv("MEMGRAPH_PASSWORD")
)

db.connect()

edges = load_wiki_vote("datasets/Wiki-Vote.txt")

print(f"Loaded {len(edges)} relationships")

start = time.perf_counter()

db.insert_edges(edges)

elapsed = time.perf_counter() - start

nodes = db.count_nodes()
relationships = db.count_relationships()
throughput = len(edges) / elapsed

print(f"Insertion Time: {elapsed:.2f} seconds")
print(f"Nodes: {nodes}")
print(f"Relationships: {relationships}")
print(f"Throughput: {throughput:.2f} relationships/sec")

os.makedirs("results", exist_ok=True)
with open("results/memgraph_ingestion.csv", "w", newline="", encoding="utf-8") as file:
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
        "Memgraph",
        nodes,
        relationships,
        1000,
        round(elapsed, 3),
        round(throughput, 2)
    ])

print("Saved ingestion summary to results/memgraph_ingestion.csv")

db.close()
