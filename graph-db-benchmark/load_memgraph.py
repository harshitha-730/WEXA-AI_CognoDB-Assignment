from dotenv import load_dotenv
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

end = time.perf_counter()

print(f"Insertion Time: {end - start:.2f} seconds")

db.close()