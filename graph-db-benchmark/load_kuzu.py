import csv, time, os

def prep_csvs(src_path="datasets/Wiki-Vote.txt",
              nodes_out="datasets/kuzu_nodes.csv",
              edges_out="datasets/kuzu_edges.csv"):
    edges = []
    node_ids = set()
    with open(src_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            s, d = line.strip().split()
            s, d = int(s), int(d)
            edges.append((s, d))
            node_ids.add(s)
            node_ids.add(d)

    with open(nodes_out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id"])
        for nid in sorted(node_ids):
            w.writerow([nid])

    with open(edges_out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["src", "dst"])
        for s, d in edges:
            w.writerow([s, d])

    return len(node_ids), len(edges)


if __name__ == "__main__":
    try:
        import kuzu  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "Kùzu is not available in the current Python environment. "
            "Activate `kuzu_venv` and install the `kuzu` package before running."
        ) from exc

    n_nodes, n_edges = prep_csvs()
    print(f"Prepared CSVs: {n_nodes} nodes, {n_edges} edges")

    db_path = "kuzu_db"
    if os.path.exists(db_path):
        import shutil
        shutil.rmtree(db_path)  # fresh load each run

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