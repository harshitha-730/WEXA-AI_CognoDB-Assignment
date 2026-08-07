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

end = time.perf_counter()

print(f"Insertion Time: {end-start:.2f} seconds")

db.close()