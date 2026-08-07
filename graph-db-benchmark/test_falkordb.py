from dotenv import load_dotenv
import os

from benchmark.falkordb import FalkorDBBenchmark

load_dotenv()

db = FalkorDBBenchmark(
    host=os.getenv("FALKORDB_HOST"),
    port=int(os.getenv("FALKORDB_PORT"))
)

db.connect()

print("Nodes:", db.count_nodes())

db.close()