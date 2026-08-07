import time
import random
import statistics
import os


class KuzuBenchmark:

    def __init__(self, db_path="kuzu_db"):
        try:
            import kuzu
        except ImportError as exc:
            raise ImportError(
                "Kùzu is not available. Activate kuzu_venv "
                "and install the kuzu package."
            ) from exc

        self.db_path = db_path
        self.db = kuzu.Database(db_path)
        self.conn = kuzu.Connection(self.db)
        self.node_ids = []

    # -------------------------
    # Connection
    # -------------------------

    def connect(self):
        print("✅ Connected to Kùzu")

    def close(self):
        print("🔒 Connection Closed")

    # -------------------------
    # Query executor
    # -------------------------

    def execute_query(self, query):
        result = self.conn.execute(query)

        rows = []

        while result.has_next():
            rows.append(result.get_next())

        return rows

    # -------------------------
    # Counts
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
    # Load node IDs
    # -------------------------

    def load_node_ids(self, limit=5000):

        rows = self.execute_query(
            f"""
            MATCH (n:User)
            RETURN n.id
            LIMIT {limit}
            """
        )

        self.node_ids = [row[0] for row in rows]

    # -------------------------
    # Point lookup
    # -------------------------

    def lookup_user(self, user_id):

        return self.execute_query(
            f"""
            MATCH (u:User {{id:{user_id}}})
            RETURN u
            """
        )

    # -------------------------
    # Aggregation
    # -------------------------

    def aggregation(self):

        return self.execute_query(
            """
            MATCH (u:User)-[:VOTED_FOR]->()
            RETURN u.id, count(*) AS c
            ORDER BY c DESC
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
    # Point lookup benchmark
    # -------------------------

    def bench_point_lookup(self, n=100):

        def run():

            uid = random.choice(self.node_ids)

            self.lookup_user(uid)

        return self._time_n(run, n)

    # -------------------------
    # Filtered lookup benchmark
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
    # Aggregation benchmark
    # -------------------------

    def bench_aggregation(self, n=100):

        return self._time_n(
            self.aggregation,
            n
        )

    # -------------------------
    # Disk footprint
    # -------------------------

    def footprint(self, db_path=None):

        if db_path is None:
            db_path = self.db_path

        total = 0

        # Kùzu is currently stored as a single
        # database file in this benchmark.
        if os.path.isfile(db_path):

            total = os.path.getsize(db_path)

        # Also support directory-based Kùzu
        # database layouts if used in another setup.
        elif os.path.isdir(db_path):

            for root, _, files in os.walk(db_path):

                for filename in files:

                    filepath = os.path.join(
                        root,
                        filename
                    )

                    total += os.path.getsize(filepath)

        return {
            "on_disk_size_bytes": total,
            "on_disk_size_human":
                f"{total / 1e6:.2f}MB",

            "note": (
                "Kùzu is embedded; memory is not "
                "exposed via API. Reporting "
                "on-disk database size instead."
            )
        }