# Graph DB Benchmark

This repository compares Neo4j, Memgraph, FalkorDB, and Kùzu for graph query performance using the Wiki-Vote dataset.

## Repository structure

- `benchmark/` - DB benchmark classes and query implementations.
- `datasets/` - Input dataset and CSV files for Kùzu.
- `kuzu_venv/` - Separate virtual environment for Kùzu dependencies.
- `results/` - Generated benchmark CSV files and plot outputs.
- `utils/` - Shared benchmark helpers.
- `load_*.py` - Dataset ingest scripts for each database.
- `*_benchmark.py` - Benchmark runners for each database.
- `compare_results.py` - Merges raw result CSVs into `results/final_comparison.csv`.
- `visualize_results.py` - Generates comparison plots in `results/plots/`.
- `.env` - Environment variables for Neo4j, Memgraph, FalkorDB, and CognoDB.

## Setup

### 1. Python environment

Create and activate a Python environment for the main repository:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Kùzu environment

Kùzu requires Python 3.12 and is installed in a separate virtual environment because its package can clash with the main workspace environment.

```powershell
python -m venv kuzu_venv
kuzu_venv\Scripts\activate
pip install -r requirements.txt
pip install kuzu
```

> Use `kuzu_venv` only for Kùzu-related steps.
> If you see an import error for `kuzu`, make sure `kuzu_venv` is active and that the environment is running Python 3.12.
>
> Verify the Kùzu environment with:
>
> ```powershell
> kuzu_venv\Scripts\activate
> python --version
> ```
>
> The output should show Python 3.12.x.

### 3. Environment variables

Create a `.env` file in the project root with the following variables:

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

Adjust these values to your local deployment.

## Data loading

### 1. Load Neo4j

```powershell
venv\Scripts\activate
python load_neo4j.py
```

### 2. Load Memgraph

```powershell
venv\Scripts\activate
python load_memgraph.py
```

### 3. Load FalkorDB

```powershell
venv\Scripts\activate
python load_falkordb.py
```

### 4. Load Kùzu

```powershell
kuzu_venv\Scripts\activate
python load_kuzu.py
```

### 5. Load CognoDB

```powershell
venv\Scripts\activate
python load_data.py
```

## Benchmark execution

### 1. Run database-specific benchmarks

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

### 2. Combine results

```powershell
venv\Scripts\activate
python compare_results.py
```

### 3. Generate plots

```powershell
venv\Scripts\activate
python visualize_results.py
```

Plots are saved to `results/plots/`.

## Quick validation tests

The repository includes simple connectivity checks for each database:

```powershell
venv\Scripts\activate
python test_neo4j.py
python test_memgraph.py
python test_falkordb.py
```

Kùzu has no dedicated test script, but `load_kuzu.py` and `kuzu_benchmark.py` perform the required database initialization and query execution.

## Result files

- `results/neo4j_results.csv`
- `results/memgraph_results.csv`
- `results/falkordb_results.csv`
- `results/kuzu_results.csv`
- `results/final_comparison.csv`
- `results/plots/aggregation_comparison.png`
- `results/plots/lookup_comparison.png`
- `results/plots/traversal_comparison.png`

## Benchmark observations

The current benchmark output shows:

- **Aggregation:** Kùzu is the fastest with `~20.16 ms`, followed by Memgraph (`~41.96 ms`), Neo4j (`~38.77 ms`), and FalkorDB is the slowest at `~61.42 ms`.
- **Point lookup:** Kùzu leads with `~0.85 ms`, while FalkorDB is around `2.25 ms`, Memgraph at `4.15 ms`, and Neo4j at `10.18 ms`.
- **Filtered lookup:** Kùzu is best (`~0.92 ms`), then FalkorDB (`~2.29 ms`), Memgraph (`~4.10 ms`), and Neo4j (`~8.36 ms`).
- **Traversal:** FalkorDB performs best for 1-hop (`~2.72 ms`) and 2-hop (`~2.45 ms`) traversal. Kùzu wins 1-hop at `~1.81 ms`, but Neo4j and Memgraph are slower for all hops.
- **3-hop traversal:** FalkorDB is the fastest among the general graph DBs at `~2.99 ms`, while Kùzu slows to `~9.84 ms`.

### Winner summary by metric

| Metric | Winner |
|---|---|
| Point lookup | Kùzu |
| Filtered lookup | Kùzu |
| 1-hop traversal | Kùzu |
| 2-hop traversal | FalkorDB |
| 3-hop traversal | FalkorDB |
| Aggregation | Kùzu |

> Kùzu is consistently fastest for lookup and aggregation, while FalkorDB has the best multi-hop traversal latency in this dataset.

## Notes

- `results/final_comparison.csv` is the merged comparison source.
- `results/plots/` contains the generated charts.
- The `kuzu_venv` folder exists because Kùzu requires an isolated Python environment.
- `requirements.txt` should include generic packages for plotting and CSV handling; Kùzu-specific installation is separate.
- See `ASSIGNMENT_REPORT.md` for a short benchmark report and winner summary.

## Known limitations

- The benchmark uses a single dataset and may not reflect other graph shapes or sizes.
- Kùzu runs as an embedded local database, while Neo4j, Memgraph, and FalkorDB use networked drivers.
- No explicit cold-start warming or indexing strategy is enforced beyond the script defaults.
- Results are from the current code path and may vary with different configuration or hardware.

## Dependencies

Install required packages with:

```powershell
pip install -r requirements.txt
```
