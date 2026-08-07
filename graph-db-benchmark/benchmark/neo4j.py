from neo4j import GraphDatabase


class Neo4jBenchmark:

    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    # ----------------------------
    # Connection Methods
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
            result = session.run(query, parameters or {})
            return list(result)

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

                session.run(query, edges=formatted_edges)

                print(f"Inserted {min(i + batch_size, total)} / {total}")

    # ----------------------------
    # Benchmark Queries
    # ----------------------------

    def count_nodes(self):
        query = """
        MATCH (n:User)
        RETURN count(n) AS total
        """

        result = self.execute_query(query)
        return result[0]["total"]

    def count_relationships(self):
        query = """
        MATCH ()-[r:VOTED_FOR]->()
        RETURN count(r) AS total
        """

        result = self.execute_query(query)
        return result[0]["total"]

    def lookup_user(self, user_id):
        query = """
        MATCH (u:User {id:$id})
        RETURN u
        """

        return self.execute_query(query, {"id": user_id})

    def traverse(self, user_id):
        query = """
        MATCH (u:User {id:$id})-[:VOTED_FOR]->(friend)
        RETURN friend
        """

        return self.execute_query(query, {"id": user_id})

    def aggregation(self):
        query = """
        MATCH (u:User)-[:VOTED_FOR]->()
        RETURN u.id AS user_id, count(*) AS votes
        ORDER BY votes DESC
        LIMIT 10
        """

        return self.execute_query(query)