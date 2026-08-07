import time

from benchmark.cognodb import CognoDBBenchmark
from utils.loader import load_wiki_vote

db = CognoDBBenchmark()

db.connect()

edges = load_wiki_vote("datasets/Wiki-Vote.txt")

print(f"Loaded {len(edges)} relationships")

start = time.perf_counter()

db.insert_edges(edges)

end = time.perf_counter()

print(f"Insertion Time: {end-start:.2f} seconds")

db.close()