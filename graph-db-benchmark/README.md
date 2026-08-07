# Graph DB Benchmark

This repository contains a reproducible benchmark of Neo4j, Memgraph, FalkorDB, Kùzu, and CognoDB using the Wiki-Vote graph dataset.

> **Evaluator note:** This README is the canonical project documentation and is intentionally the same at both the repository root and inside `graph-db-benchmark/`.

---

## Objective

- Ingest the Wiki-Vote dataset into multiple graph databases.
- Measure query latency for point lookup, filtered lookup, traversal, and aggregation.
- Compare results across systems and report the winner for each workload.
- Capture ingestion throughput, footprint metrics, and dataset provenance.

---

## Dataset

- Name: Wiki-Vote
- Source: https://snap.stanford.edu/data/wiki-Vote.html
- Nodes: 7,115
- Relationships: 103,689
- Relationship type: `VOTED_FOR`

---

## Project structure

- `benchmark/` - database benchmark classes and query implementations
- `datasets/` - input dataset and generated Kùzu CSV files
- `load_*.py` - ingestion scripts for Neo4j, Memgraph, FalkorDB, Kùzu, and CognoDB
- `*_benchmark.py` - benchmark runners for each database platform
- `compare_results.py` - merges benchmark results into `results/final_comparison.csv`
- `visualize_results.py` - generates charts under `results/plots/`
- `ASSIGNMENT_REPORT.md` - concise benchmark report and observations
- `requirements.txt` - Python dependencies for the benchmark
- `.gitignore` - excludes virtual environments and generated artifacts

---

## Setup

### 1. Main environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Kùzu environment

Kùzu requires Python 3.12, so it is installed in a separate environment.

```powershell
python -m venv kuzu_venv
kuzu_venv\Scripts\activate
pip install -r requirements.txt
pip install kuzu
```

> If `kuzu` import fails, activate `kuzu_venv` and verify Python:
>
> ```powershell
> kuzu_venv\Scripts\activate
> python --version
> ```
>
> It should report Python 3.12.x.

---

## Environment variables

Create a `.env` file in the repository root with the following values:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

MEMGRAPH_URI=bolt://localhost:7687
MEMGRAPH_USERNAME=memgraph
MEMGRAPH_PASSWORD=password

FALKORDB_HOST=localhost
FALKORDB_PORT=6379

COGNODB_URI=bolt://localhost:7687
COGNODB_USERNAME=admin
COGNODB_PASSWORD=password
```

Update the values to match your deployment.

---

## Data ingestion

Load the dataset into each database from inside `graph-db-benchmark/`:

```powershell
venv\Scripts\activate
python load_neo4j.py
python load_memgraph.py
python load_falkordb.py
python load_data.py
```

For Kùzu:

```powershell
kuzu_venv\Scripts\activate
python load_kuzu.py
```

Each ingestion script writes a summary CSV to `results/` including insertion time and throughput.

---

## Run benchmarks

From inside `graph-db-benchmark/`:

```powershell
venv\Scripts\activate
python neo4j_benchmark.py
python memgraph_benchmark.py
python falkordb_benchmark.py
python cognodb_benchmark.py
```

For Kùzu:

```powershell
kuzu_venv\Scripts\activate
python kuzu_benchmark.py
```

Each benchmark captures point lookup, filtered lookup, 1-hop/2-hop/3-hop traversal, and aggregation latency metrics (p50/p95).

---

## Combine results and visualize

```powershell
venv\Scripts\activate
python compare_results.py
python visualize_results.py
```

Generated charts are saved in `results/plots/`.

---

## Validation tests

```powershell
venv\Scripts\activate
python test_neo4j.py
python test_memgraph.py
python test_falkordb.py
```

> Kùzu does not have a dedicated test script; use `load_kuzu.py` and `kuzu_benchmark.py` to verify Kùzu.

---

## Result files

- `results/neo4j_results.csv`
- `results/memgraph_results.csv`
- `results/falkordb_results.csv`
- `results/kuzu_results.csv`
- `results/cognodb_results.csv`
- `results/final_comparison.csv`
- `results/plots/aggregation_comparison.png`
- `results/plots/lookup_comparison.png`
- `results/plots/traversal_comparison.png`
- `results/*_ingestion.csv`

---

## Measured metrics

- Point lookup latency (p50 / p95)
- Filtered lookup latency (p50 / p95)
- Traversal latency for 1-hop, 2-hop, and 3-hop paths (p50 / p95)
- Aggregation latency (p50 / p95)
- Ingestion throughput
- Dataset provenance
- Footprint reporting when available

---

## Notes on fairness and compliance

This benchmark uses the same dataset and comparable query workloads across all tested systems.

- The same Wiki-Vote dataset is used for every database.
- Query definitions are aligned across systems.
- Footprint metrics are included where the database exposes them.
- Kùzu is embedded locally, while Neo4j, Memgraph, FalkorDB, and CognoDB are accessed via standard client drivers.

---

## Known limitations

- Only one dataset is used for this take-home benchmark.
- Full cloud-managed free-tier deployment was not part of the local repository execution environment.
- Kùzu is embedded; other systems are benchmarked using network drivers.
- Memory/disk footprint may be unavailable for some systems due to driver/API limitations.

---

## Dependencies

```powershell
pip install -r requirements.txt
```
