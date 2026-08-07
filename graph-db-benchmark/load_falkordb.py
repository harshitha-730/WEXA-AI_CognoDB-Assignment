import time, os
from dotenv import load_dotenv
from benchmark.falkordb import FalkorDBBenchmark

load_dotenv()

def load_wiki_vote_edges(path="datasets/Wiki-Vote.txt"):
    edges = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            src, dst = line.strip().split()
            edges.append((int(src), int(dst)))
    return edges

if __name__ == "__main__":
    db = FalkorDBBenchmark(
        host=os.getenv("FALKORDB_HOST"),
        port=int(os.getenv("FALKORDB_PORT")),
    )
    edges = load_wiki_vote_edges()
    print(f"Read {len(edges)} edges from file")

    elapsed, nodes, rels = db.insert_edges(edges)
    print(f"Ingest time: {elapsed:.2f}s")
    print(f"Nodes: {nodes} ({nodes/elapsed:.1f}/s)  Relationships: {rels} ({rels/elapsed:.1f}/s)")