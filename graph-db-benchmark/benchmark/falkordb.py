from falkordb import FalkorDB
import time
import random
import statistics


class FalkorDBBenchmark:

    def __init__(self, host="localhost", port=6379):
        self.db = FalkorDB(host=host, port=port)
        self.graph = self.db.select_graph("benchmark")
        self.node_ids = []

    # -------------------------
    # Connection
    # -------------------------

    def connect(self):
        print("✅ Connected to FalkorDB")

    def close(self):
        print("🔒 Connection Closed")

    # -------------------------
    # Generic query executor
    # -------------------------

    def execute_query(self, query, params=None):
        result = self.graph.query(query, params or {})
        return result.result_set

    # -------------------------
    # Dataset / counts
    # -------------------------

    def count_nodes(self):
        return self.execute_query(
            "MATCH (n:User) RETURN count(n)"
        )[0][0]

    def count_relationships(self):
        return self.execute_query(
            "MATCH ()-[r:VOTED_FOR]->() RETURN count(r)"
        )[0][0]

    # -------------------------
    # Basic queries
    # -------------------------

    def lookup_user(self, user_id):
        return self.execute_query(
            f"""
            MATCH (u:User {{id:{user_id}}})
            RETURN u
            """
        )

    def traverse(self, user_id):
        return self.execute_query(
            f"""
            MATCH (u:User {{id:{user_id}}})
            -[:VOTED_FOR]->(friend)
            RETURN friend
            """
        )

    def aggregation(self):
        return self.execute_query(
            """
            MATCH (u:User)-[:VOTED_FOR]->()
            RETURN u.id, count(*) AS votes
            ORDER BY votes DESC
            LIMIT 10
            """
        )

    # -------------------------
    # Timing helper
    # -------------------------

    def _time_n(self, fn, n=100):

        latencies = []

        for _ in range(n):

            start = time.perf_counter()

            fn()

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            latencies.append(elapsed)

        latencies.sort()

        p50 = statistics.median(latencies)

        p95_index = max(
            0,
            int(len(latencies) * 0.95) - 1
        )

        p95 = latencies[p95_index]

        return (
            round(p50, 3),
            round(p95, 3)
        )

    # -------------------------
    # Traversal benchmark
    # -------------------------

    def bench_traversal(self, hops, n=100):

        pattern = "-[:VOTED_FOR]->()" * hops

        def run():

            uid = random.choice(self.node_ids)

            self.execute_query(
                f"""
                MATCH (u:User {{id:{uid}}})
                {pattern}
                RETURN count(*)
                """
            )

        return self._time_n(run, n)

    # -------------------------
    # Point lookup
    # -------------------------

    def bench_point_lookup(self, n=100):

        def run():

            uid = random.choice(self.node_ids)

            self.lookup_user(uid)

        return self._time_n(run, n)

    # -------------------------
    # Filtered lookup
    # -------------------------

    def bench_filtered_lookup(self, n=100):

        def run():

            uid = random.choice(self.node_ids)

            self.execute_query(
                f"""
                MATCH (u:User)
                WHERE u.id = {uid}
                RETURN u
                """
            )

        return self._time_n(run, n)

    # -------------------------
    # Aggregation
    # -------------------------

    def bench_aggregation(self, n=100):

        return self._time_n(
            self.aggregation,
            n
        )

    # -------------------------
    # Memory footprint
    # -------------------------

    def footprint(self):

        try:

            info = self.db.connection.info("memory")

            return {
                "used_memory_human":
                    info.get("used_memory_human"),

                "used_memory_bytes":
                    info.get("used_memory")
            }

        except Exception:

            return {
                "used_memory_human": "N/A",
                "used_memory_bytes": "N/A"
            }