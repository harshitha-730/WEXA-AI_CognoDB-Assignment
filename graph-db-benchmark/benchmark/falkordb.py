from falkordb import FalkorDB
import time, random, statistics


class FalkorDBBenchmark:

    def __init__(self, host="localhost", port=6379):
        self.db = FalkorDB(host=host, port=port)
        self.graph = self.db.select_graph("benchmark")
        self.node_ids = []

    # ---------------- Connection ----------------
    def connect(self):
        print("✅ Connected to FalkorDB")

    def close(self):
        print("🔒 Connection Closed")

    def execute_query(self, query, params=None):
        result = self.graph.query(query, params)
        return result.result_set

    # ---------------- Dataset Loading (bulk, batched) ----------------
    def insert_edges(self, edges, batch_size=1000):
        start = time.perf_counter()
        for i in range(0, len(edges), batch_size):
            batch = edges[i:i + batch_size]
            rows = [{"src": s, "dst": d} for s, d in batch]
            self.execute_query(
                """
                UNWIND $rows AS row
                MERGE (u1:User {id: row.src})
                MERGE (u2:User {id: row.dst})
                MERGE (u1)-[:VOTED_FOR]->(u2)
                """,
                {"rows": rows},
            )
            if (i // batch_size) % 10 == 0:
                print(f"Inserted {i + len(batch)} / {len(edges)}")
        elapsed = time.perf_counter() - start

        # index for filtered/indexed lookup requirement
        self.execute_query("CREATE INDEX FOR (n:User) ON (n.id)")

        node_count = self.count_nodes()
        rel_count = self.count_relationships()
        self.node_ids = [r[0] for r in self.execute_query(
            "MATCH (n:User) RETURN n.id LIMIT 5000")]
        return elapsed, node_count, rel_count

    # ---------------- Basic queries (unchanged names) ----------------
    def count_nodes(self):
        return self.execute_query("MATCH (n:User) RETURN count(n)")[0][0]

    def count_relationships(self):
        return self.execute_query("MATCH ()-[r:VOTED_FOR]->() RETURN count(r)")[0][0]

    def lookup_user(self, user_id):
        return self.execute_query(f"MATCH (u:User {{id:{user_id}}}) RETURN u")

    def traverse(self, user_id):
        return self.execute_query(
            f"MATCH (u:User {{id:{user_id}}})-[:VOTED_FOR]->(friend) RETURN friend"
        )

    def aggregation(self):
        return self.execute_query(
            """
            MATCH (u:User)-[:VOTED_FOR]->()
            RETURN u.id, count(*) ORDER BY count(*) DESC LIMIT 10
            """
        )

    # ---------------- Timed benchmark helpers ----------------
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

    def footprint(self):
        info = self.db.connection.info("memory")
        return {"used_memory_human": info.get("used_memory_human"),
                "used_memory_bytes": info.get("used_memory")}