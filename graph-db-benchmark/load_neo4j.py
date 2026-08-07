import csv
import os
import time
from dotenv import load_dotenv

from benchmark.neo4j import Neo4jBenchmark
from utils.loader import load_wiki_vote

load_dotenv()

db = Neo4jBenchmark(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD")
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
with open("results/neo4j_ingestion.csv", "w", newline="", encoding="utf-8") as file:
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
        "Neo4j",
        nodes,
        relationships,
        1000,
        round(elapsed, 3),
        round(throughput, 2)
    ])

print("Saved ingestion summary to results/neo4j_ingestion.csv")

db.close()
