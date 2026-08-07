from .neo4j import Neo4jBenchmark


class MemgraphBenchmark(Neo4jBenchmark):
    """
    Memgraph uses the same Bolt driver and Cypher syntax
    for the operations in this assignment, so we inherit
    everything from Neo4jBenchmark.
    """
    pass