from neo4j import GraphDatabase


class Neo4jBenchmark:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    # ----------------------------
    # Connection
    # ----------------------------

    def connect(self):
        self.driver.verify_connectivity()
        print("✅ Connected to Neo4j")

    def close(self):
        self.driver.close()
        print("🔒 Connection Closed")

    # ----------------------------
    # Generic Query Executor
    # ----------------------------

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(
                query,
                parameters or {}
            )
            return list(result)

    # ----------------------------
    # Schema
    # ----------------------------

    def create_index(self):
        query = """
        CREATE INDEX user_id_index IF NOT EXISTS
        FOR (n:User)
        ON (n.id)
        """

        self.execute_query(query)
        print("✅ User.id index created/verified")

    # ----------------------------
    # Clear Database
    # ----------------------------

    def clear_graph(self):
        self.execute_query(
            """
            MATCH (n:User)
            DETACH DELETE n
            """
        )

    # ----------------------------
    # Dataset Loading
    # ----------------------------

    def insert_edges(self, edges, batch_size=1000):

        query = """
        UNWIND $edges AS edge

        MERGE (u1:User {id: edge.source})
        MERGE (u2:User {id: edge.target})

        MERGE (u1)-[:VOTED_FOR]->(u2)
        """

        total = len(edges)

        with self.driver.session() as session:

            for i in range(0, total, batch_size):

                batch = edges[i:i + batch_size]

                formatted_edges = [
                    {
                        "source": source,
                        "target": target
                    }
                    for source, target in batch
                ]

                result = session.run(
                    query,
                    edges=formatted_edges
                )

                # Force the database to finish the query
                result.consume()

                print(
                    f"Inserted "
                    f"{min(i + batch_size, total)} / {total}"
                )

    # ----------------------------
    # Counts
    # ----------------------------

    def count_nodes(self):

        result = self.execute_query(
            """
            MATCH (n:User)
            RETURN count(n) AS total
            """
        )

        return result[0]["total"]

    def count_relationships(self):

        result = self.execute_query(
            """
            MATCH ()-[r:VOTED_FOR]->()
            RETURN count(r) AS total
            """
        )

        return result[0]["total"]

    # ----------------------------
    # Queries
    # ----------------------------

    def lookup_user(self, user_id):

        query = """
        MATCH (u:User {id: $id})
        RETURN u
        """

        return self.execute_query(
            query,
            {"id": user_id}
        )

    def filtered_lookup(self, user_id):

        query = """
        MATCH (u:User)
        WHERE u.id = $id
        RETURN u
        """

        return self.execute_query(
            query,
            {"id": user_id}
        )

    def traverse(self, user_id):

        query = """
        MATCH (u:User {id: $id})
              -[:VOTED_FOR]->
              (friend)
        RETURN friend
        """

        return self.execute_query(
            query,
            {"id": user_id}
        )

    def aggregation(self):

        query = """
        MATCH (u:User)-[:VOTED_FOR]->()

        RETURN
            u.id AS user_id,
            count(*) AS votes

        ORDER BY votes DESC
        LIMIT 10
        """

        return self.execute_query(query)

    # ----------------------------
    # Warm-up
    # ----------------------------

    def warmup(self, user_id=30):

        self.lookup_user(user_id)
        self.filtered_lookup(user_id)
        self.traverse(user_id)
        self.aggregation()

        print("🔥 Warm-up completed")