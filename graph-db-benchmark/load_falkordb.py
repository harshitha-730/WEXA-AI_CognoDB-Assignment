import csv
import os
import time
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
    throughput = rels / elapsed

    print(f"Ingest time: {elapsed:.2f}s")
    print(f"Nodes: {nodes} ({nodes/elapsed:.1f}/s)  Relationships: {rels} ({rels/elapsed:.1f}/s)")

    os.makedirs("results", exist_ok=True)
    with open("results/falkordb_ingestion.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "platform",
            "node_count",
            "rel_count",
            "insertion_time_s",
            "ingestion_throughput_rel_s"
        ])
        writer.writerow([
            "FalkorDB",
            nodes,
            rels,
            round(elapsed, 3),
            round(throughput, 2)
        ])

    print("Saved ingestion summary to results/falkordb_ingestion.csv")
