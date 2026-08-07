from dotenv import load_dotenv
import os

from benchmark.memgraph import MemgraphBenchmark

load_dotenv()

db = MemgraphBenchmark(
    os.getenv("MEMGRAPH_URI"),
    os.getenv("MEMGRAPH_USERNAME"),
    os.getenv("MEMGRAPH_PASSWORD")
)

db.connect()

print("Nodes:", db.count_nodes())

db.close()