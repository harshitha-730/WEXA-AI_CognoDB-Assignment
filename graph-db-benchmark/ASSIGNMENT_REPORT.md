# Assignment Benchmark Report

## Overview

This report summarizes the graph database benchmark results from the Wiki-Vote dataset.
Benchmarked systems: Neo4j, Memgraph, FalkorDB, Kùzu, and CognoDB.

Dataset:
- Name: Wiki-Vote
- Source: https://snap.stanford.edu/data/wiki-Vote.html
- Nodes: 7,115
- Relationships: 103,689
- Relationship type: VOTED_FOR

## Benchmark goals

The benchmark covers:
- Data ingestion throughput
- Point lookup latency
- Filtered lookup latency
- 1-hop, 2-hop, 3-hop traversal latency
- Aggregation query latency
- Footprint and resource metrics where available

## Results

- **Kùzu** is the best performer for point lookup, filtered lookup, and aggregation.
- **FalkorDB** is the best performer for 2-hop and 3-hop traversal latency.
- **Memgraph** is stable in the mid-range.
- **Neo4j** is the slowest on this dataset and workload.

## Winner summary

| Metric | Winner |
|---|---|
| Point lookup | Kùzu |
| Filtered lookup | Kùzu |
| 1-hop traversal | Kùzu |
| 2-hop traversal | FalkorDB |
| 3-hop traversal | FalkorDB |
| Aggregation | Kùzu |

## Compliance notes

- The benchmark uses the same Wiki-Vote dataset for all systems.
- Query workloads are consistent across platforms.
- Ingestion throughput measurement is included for Neo4j, Memgraph, FalkorDB, Kùzu, and CognoDB.
- p50/p95 latency metrics are measured for each database.
- Where possible, footprint metrics are recorded.

## Known limitations

- Cloud-managed free-tier deployments are not part of the local benchmark execution.
- Kùzu is benchmarked as an embedded local database, while the other systems use client drivers.
- Resource usage reporting is limited by the APIs exposed by each database.
