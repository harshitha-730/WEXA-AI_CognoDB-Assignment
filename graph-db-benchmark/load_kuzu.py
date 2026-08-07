import csv
import os
import time


def prep_csvs(src_path="datasets/Wiki-Vote.txt",
              nodes_out="datasets/kuzu_nodes.csv",
              edges_out="datasets/kuzu_edges.csv"):
    edges = []
    node_ids = set()

    with open(src_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue

            s, d = line.strip().split()
            s, d = int(s), int(d)

            edges.append((s, d))
            node_ids.add(s)
            node_ids.add(d)

    with open(nodes_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id"])
        for nid in sorted(node_ids):
            writer.writerow([nid])

    with open(edges_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["src", "dst"])
        for s, d in edges:
            writer.writerow([s, d])

    return len(node_ids), len(edges)


if __name__ == "__main__":
    try:
        import kuzu  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "Kùzu is not available in the current Python environment. "
            "Activate kuzu_venv and install the kuzu package before running."
        ) from exc

    n_nodes, n_edges = prep_csvs()
    print(f"Prepared CSVs: {n_nodes} nodes, {n_edges} edges")

    db_path = "kuzu_db"
    if os.path.exists(db_path):
        import shutil
        shutil.rmtree(db_path)

    db = kuzu.Database(db_path)
    conn = kuzu.Connection(db)

    conn.execute("CREATE NODE TABLE User(id INT64, PRIMARY KEY(id))")
    conn.execute("CREATE REL TABLE VOTED_FOR(FROM User TO User)")

    start = time.perf_counter()
    conn.execute('COPY User FROM "datasets/kuzu_nodes.csv" (HEADER=true)')
    conn.execute('COPY VOTED_FOR FROM "datasets/kuzu_edges.csv" (HEADER=true)')
    elapsed = time.perf_counter() - start

    print(f"Ingest time: {elapsed:.2f}s")
    print(f"Nodes/s: {n_nodes/elapsed:.1f}  Rels/s: {n_edges/elapsed:.1f}")

    os.makedirs("results", exist_ok=True)
    with open("results/kuzu_ingestion.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "platform",
            "node_count",
            "rel_count",
            "ingestion_time_s",
            "ingestion_throughput_rel_s"
        ])
        writer.writerow([
            "Kùzu",
            n_nodes,
            n_edges,
            round(elapsed, 3),
            round(n_edges / elapsed, 2)
        ])

    print("Saved ingestion summary to results/kuzu_ingestion.csv")
