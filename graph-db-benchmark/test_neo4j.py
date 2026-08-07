from dotenv import load_dotenv
import os

from benchmark.neo4j import Neo4jBenchmark

load_dotenv()

db = Neo4jBenchmark(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD")
)

db.connect()

print("Nodes:", db.count_nodes())

db.close()