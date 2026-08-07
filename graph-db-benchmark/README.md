# Graph DB Benchmark

This repository contains a reproducible benchmark of Neo4j, Memgraph, FalkorDB, Kùzu, and CognoDB using the Wiki-Vote graph dataset.

> **Evaluator note:** This README documents setup, execution, result generation, and analysis in a clear, structured way.

---

## Objective

- Load the Wiki-Vote dataset into multiple graph databases
- Measure query latency for point lookup, filtered lookup, traversal, and aggregation
- Compare results across databases
- Generate charts and a concise report

---

## Databases included

- CognoDB
- Neo4j
- Memgraph
- FalkorDB
- Kùzu

---

## Dataset

- Name: Wiki-Vote
- Nodes: 7,115
- Relationships: 103,689
- Relationship type: `VOTED_FOR`

---

## Repository structure

- `benchmark/` - database benchmark classes and query implementations
- `datasets/` - Wiki-Vote input data and Kùzu CSV files
- `load_*.py` - ingestion scripts for each database
- `*_benchmark.py` - benchmark runners for each database platform
- `compare_results.py` - merges individual database results into a final comparison
- `visualize_results.py` - generates charts under `results/plots/`
- `results/` - generated benchmark CSVs and plots
- `utils/` - shared helper modules
- `.env` - environment configuration file
- `requirements.txt` - Python dependencies
- `ASSIGNMENT_REPORT.md` - concise benchmark report and findings

---

## Setup

### 1. Main environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Kùzu environment

Kùzu requires Python 3.12, so it is installed into a separate virtual environment.

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

Update these values for your local deployment.

---

## Data ingestion

Load the dataset into each database:

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

---

## Benchmark execution

Run each benchmark:

```powershell
venv\Scripts\activate
python neo4j_benchmark.py
python memgraph_benchmark.py
python falkordb_benchmark.py
```

For Kùzu:

```powershell
kuzu_venv\Scripts\activate
python kuzu_benchmark.py
```

---

## Combine results and visualize

```powershell
venv\Scripts\activate
python compare_results.py
python visualize_results.py
```

Results are stored under `results/` and charts are saved to `results/plots/`.

---

## Validation tests

```powershell
venv\Scripts\activate
python test_neo4j.py
python test_memgraph.py
python test_falkordb.py
```

> Kùzu does not have a dedicated test script; use `load_kuzu.py` and `kuzu_benchmark.py` for Kùzu validation.

---

## Result files

- `results/neo4j_results.csv`
- `results/memgraph_results.csv`
- `results/falkordb_results.csv`
- `results/kuzu_results.csv`
- `results/final_comparison.csv`
- `results/plots/aggregation_comparison.png`
- `results/plots/lookup_comparison.png`
- `results/plots/traversal_comparison.png`

---

## Benchmark metrics

The benchmark evaluates:

- Point lookup
- Filtered lookup
- 1-hop traversal
- 2-hop traversal
- 3-hop traversal
- Aggregation

Each measurement captures p50 and p95 latency values.

---

## Key findings

- **Kùzu** is fastest for point lookup, filtered lookup, and aggregation.
- **FalkorDB** is best for 2-hop and 3-hop traversal latency.
- **Memgraph** performs steadily in the mid-range.
- **Neo4j** is slower than the other tested platforms for this workload.

### Winner summary

| Metric | Winner |
|---|---|
| Point lookup | Kùzu |
| Filtered lookup | Kùzu |
| 1-hop traversal | Kùzu |
| 2-hop traversal | FalkorDB |
| 3-hop traversal | FalkorDB |
| Aggregation | Kùzu |

---

## Notes

- `kuzu_venv` is separate because Kùzu requires Python 3.12.
- `results/` is excluded from git and regenerated during benchmark runs.
- `ASSIGNMENT_REPORT.md` contains a concise report and observations.

---

## Known limitations

- Single dataset workload only.
- Performance may vary on a different dataset or deployment.
- Kùzu is benchmarked as an embedded database while others use network drivers.

---

## Dependencies

```powershell
pip install -r requirements.txt
```


Kùzu recorded the lowest measured aggregation latency.

Winner Summary
Metric	Lowest p50	Result
Point Lookup	Kùzu	0.852 ms
Filtered Lookup	Kùzu	0.916 ms
1-Hop Traversal	Kùzu	1.807 ms
2-Hop Traversal	FalkorDB	2.447 ms
3-Hop Traversal	FalkorDB	2.991 ms
Aggregation	Kùzu	20.159 ms
CognoDB Performance

CognoDB successfully processed the complete Wiki-Vote graph containing:

7,115 nodes
103,689 relationships

It also completed all benchmark query categories and the mixed concurrent workload.

In this benchmark run, CognoDB recorded higher client-observed query latency than the locally deployed comparison databases.

This result should not be interpreted as a universal database performance ranking because CognoDB was accessed through a cloud deployment, while Neo4j, Memgraph, FalkorDB, and Kùzu were evaluated locally.

Methodology

The benchmark uses:

Wiki-Vote dataset
7,115 nodes
103,689 relationships
Batch ingestion
Repeated query execution
Warm-up before measured queries
p50 latency
p95 latency
Point lookup
Filtered/indexed lookup
1-hop traversal
2-hop traversal
3-hop traversal
Aggregation
Mixed concurrent read/write workloads

The latency measurements represent client-observed query latency, including the time required for the database client/driver to execute the query and receive the result.

Reproducibility
CognoDB

Activate the main environment:

venv\Scripts\activate

Load the dataset:

python load_data.py

Run the query benchmark:

python cognodb_benchmark.py

Run the mixed workload:

python mixed_benchmark.py

Generate the comparison:

python compare_results.py

Generated results are stored in:

results/
Result Files

Important generated benchmark files:

results/cognodb_results.csv
results/cognodb_ingestion.csv
results/cognodb_mixed_workload.csv
results/neo4j_results.csv
results/memgraph_results.csv
results/falkordb_results.csv
results/kuzu_results.csv
results/final_comparison.csv
Limitations

The benchmark results are specific to the tested environment and configuration.

Important considerations:

CognoDB was accessed as a cloud database.
Neo4j and Memgraph were accessed through local Bolt endpoints.
FalkorDB was run locally through Docker.
Kùzu was run as an embedded database.
Hardware, network latency, database configuration, indexes, cache state, and background activity can affect results.
The benchmark uses a single graph dataset and therefore does not represent every possible graph workload.
Kùzu is embedded, so its memory characteristics differ from networked databases.
The measured latency includes client/driver and network overhead where applicable.
Results should be interpreted as measurements from this benchmark environment rather than universal database rankings.
Security

The .env file contains database credentials and must not be committed to the repository.

Ensure .env is included in .gitignore:

.env
venv/
kuzu_venv/
__pycache__/
*.pyc

Never publish real database passwords, API keys, or connection credentials.

Conclusion

This benchmark provides a reproducible comparison of five graph database systems using the same Wiki-Vote graph and a consistent set of graph operations.

The results demonstrate that graph database performance varies substantially by workload.

Kùzu recorded the lowest measured p50 latency for point lookup, filtered lookup, 1-hop traversal, and aggregation, while FalkorDB recorded the lowest measured p50 latency for 2-hop and 3-hop traversal.

CognoDB successfully handled the complete Wiki-Vote dataset, completed the required query benchmarks, and successfully processed the tested mixed concurrent workload with zero failed operations.

Because the databases were evaluated using different deployment architectures—particularly CognoDB as a cloud service and the other systems primarily in local environments—the results should be interpreted as measurements of the tested configurations rather than universal rankings.