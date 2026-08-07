# Assignment Benchmark Report

## Overview

This report summarizes the graph database benchmark results from the Wiki-Vote dataset.
Benchmarked systems: Neo4j, Memgraph, FalkorDB, and Kùzu.

The dataset contains 7,115 nodes and 103,689 relationships.

## Benchmark metrics

Measured metrics included:

- Point lookup latency (p50 / p95)
- Filtered lookup latency (p50 / p95)
- Traversal latency for 1-hop, 2-hop, and 3-hop queries (p50 / p95)
- Aggregation query latency (p50 / p95)
- Memory or footprint information where available

## Result highlights

- **Kùzu** is the best performer for key lookup and aggregation:
  - Point lookup: `~0.85 ms`
  - Filtered lookup: `~0.92 ms`
  - Aggregation: `~20.16 ms`
- **FalkorDB** is strongest for multi-hop traversal on this workload:
  - 1-hop traversal: `~2.72 ms`
  - 2-hop traversal: `~2.45 ms`
  - 3-hop traversal: `~2.99 ms`
- **Memgraph** provides mid-tier latency results, typically faster than Neo4j but slower than Kùzu and FalkorDB.
- **Neo4j** is the slowest across most metrics, particularly in lookup operations.

## Metric winner summary

| Metric | Winner | Notes |
|---|---|---|
| Point lookup | Kùzu | Best raw lookup latency |
| Filtered lookup | Kùzu | Fastest at both point and filter lookup |
| 1-hop traversal | Kùzu | Lowest latency in 1-hop traversal |
| 2-hop traversal | FalkorDB | Best multi-hop traversal latency |
| 3-hop traversal | FalkorDB | Best latency for deeper traversal |
| Aggregation | Kùzu | Lowest aggregation latency |

## Plot observations

### Aggregation query performance

- Kùzu shows the lowest aggregation latency.
- FalkorDB is the slowest in this category, with 60+ ms.
- Memgraph and Neo4j are closer to each other but still significantly slower than Kùzu.

### Lookup performance comparison

- Kùzu is clearly the leader for both point and filtered lookup.
- FalkorDB is competitive for lookups compared to Memgraph.
- Neo4j remains the weakest performer for both lookup patterns.

### Traversal performance comparison

- Kùzu maintains excellent 1-hop traversal performance, but its latency increases for 2-hop and 3-hop paths.
- FalkorDB is the most stable and fastest for 2-hop and 3-hop traversals.
- Memgraph is a solid mid-range performer, and Neo4j trails in all traversal depths.

## Practical takeaway

- Use **Kùzu** when lookup speed and aggregation performance are the top priority.
- Use **FalkorDB** when multi-hop traversal latency is the primary concern.
- **Memgraph** is a balanced choice but not the top-performer in any measured category.
- **Neo4j** performs adequately but is slower than the other systems for this dataset and query mix.

## Notes

- The benchmark is based on the provided dataset and the current implementation of each query.
- Actual production performance may vary based on dataset shape, cluster configuration, indexes, and runtime tuning.
- Kùzu is benchmarked using an embedded local database, while the other systems use networked drivers.
