import time, random, statistics, os


class KuzuBenchmark:

    def __init__(self, db_path="kuzu_db"):
        try:
            import kuzu  # type: ignore[import]
        except ImportError as exc:
            raise ImportError(
                "Kùzu is not available in the current Python environment. "
                "Activate `kuzu_venv` and install the `kuzu` package before running."
            ) from exc

        self.db = kuzu.Database(db_path)
        self.conn = kuzu.Connection(self.db)
        self.node_ids = []

    def connect(self):
        print("✅ Connected to Kùzu")

    def close(self):
        print("🔒 Connection Closed")

    def execute_query(self, query):
        result = self.conn.execute(query)
        rows = []
        while result.has_next():
            rows.append(result.get_next())
        return rows

    def count_nodes(self):
        return self.execute_query("MATCH (n:User) RETURN count(n)")[0][0]

    def count_relationships(self):
        return self.execute_query("MATCH ()-[r:VOTED_FOR]->() RETURN count(r)")[0][0]

    def load_node_ids(self, limit=5000):
        rows = self.execute_query(f"MATCH (n:User) RETURN n.id LIMIT {limit}")
        self.node_ids = [r[0] for r in rows]

    def lookup_user(self, user_id):
        return self.execute_query(f"MATCH (u:User {{id:{user_id}}}) RETURN u")

    def aggregation(self):
        return self.execute_query(
            """
            MATCH (u:User)-[:VOTED_FOR]->()
            RETURN u.id, count(*) AS c ORDER BY c DESC LIMIT 10
            """
        )

    def _time_n(self, fn, n=100):
        latencies = []
        for _ in range(n):
            t0 = time.perf_counter()
            fn()
            latencies.append((time.perf_counter() - t0) * 1000)
        latencies.sort()
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95) - 1]
        return round(p50, 3), round(p95, 3)

    def bench_traversal(self, hops, n=100):
        pattern = "-[:VOTED_FOR]->()" * hops

        def run():
            uid = random.choice(self.node_ids)
            self.execute_query(f"MATCH (u:User {{id:{uid}}}){pattern} RETURN count(*)")
        return self._time_n(run, n)

    def bench_point_lookup(self, n=100):
        def run():
            self.lookup_user(random.choice(self.node_ids))
        return self._time_n(run, n)

    def bench_filtered_lookup(self, n=100):
        def run():
            uid = random.choice(self.node_ids)
            self.execute_query(f"MATCH (u:User) WHERE u.id = {uid} RETURN u")
        return self._time_n(run, n)

    def bench_aggregation(self, n=100):
        return self._time_n(self.aggregation, n)

    def footprint(self, db_path="kuzu_db"):
        total = 0
        for root, _, files in os.walk(db_path):
            for f in files:
                total += os.path.getsize(os.path.join(root, f))
        return {"on_disk_size_bytes": total, "on_disk_size_human": f"{total/1e6:.2f}MB",
                "note": "Kùzu is embedded; memory not exposed via API, reporting on-disk size instead"}