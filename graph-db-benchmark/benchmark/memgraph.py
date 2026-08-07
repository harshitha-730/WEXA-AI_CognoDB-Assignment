from .neo4j import Neo4jBenchmark


class MemgraphBenchmark(Neo4jBenchmark):
    """
    Memgraph uses the Bolt protocol and Cypher.
    The query and ingestion operations are compatible
    with the Neo4j benchmark implementation.
    """

    def connect(self):
        self.driver.verify_connectivity()
        print("✅ Connected to Memgraph")

    def create_index(self):
        # Memgraph index syntax
        query = """
        CREATE INDEX ON :User(id)
        """

        try:
            self.execute_query(query)
            print("✅ Memgraph User.id index created")
        except Exception as e:
            # Index may already exist
            print(f"ℹ️ Index already exists or was not created: {e}")