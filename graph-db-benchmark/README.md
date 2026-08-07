Graph Database Benchmark

A reproducible benchmark comparing CognoDB, Neo4j, Memgraph, FalkorDB, and Kùzu using the Wiki-Vote graph dataset.

The benchmark evaluates graph ingestion performance, point lookups, filtered/indexed lookups, 1-hop/2-hop/3-hop traversals, aggregation queries, latency percentiles, and mixed concurrent workloads.

Databases

The benchmark includes:

CognoDB
Neo4j
Memgraph
FalkorDB
Kùzu
Dataset

Dataset: Wiki-Vote

The same logical graph dataset is used across the benchmarked databases.

Property	Value
Nodes	7,115
Relationships	103,689
Relationship Type	VOTED_FOR
Repository Structure
graph-db-benchmark/
│
├── benchmark/
│   ├── cognodb.py
│   ├── neo4j.py
│   ├── memgraph.py
│   ├── falkordb.py
│   └── kuzu.py
│
├── datasets/
│   └── Wiki-Vote.txt
│
├── results/
│   ├── cognodb_results.csv
│   ├── cognodb_ingestion.csv
│   ├── cognodb_mixed_workload.csv
│   ├── neo4j_results.csv
│   ├── memgraph_results.csv
│   ├── falkordb_results.csv
│   ├── kuzu_results.csv
│   └── final_comparison.csv
│
├── utils/
│
├── cognodb_benchmark.py
├── mixed_benchmark.py
├── compare_results.py
├── load_data.py
├── main.py
│
├── requirements.txt
├── README.md
└── .env
Environment Setup

Create and activate the main Python environment:

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Kùzu Environment

Kùzu can be installed in a separate environment when required by the installed Python version:

python -m venv kuzu_venv
kuzu_venv\Scripts\activate
pip install kuzu
Configuration

Database connection information is stored in .env.

Do not commit real credentials or passwords to GitHub.

Example:

COGNODB_URI=bolt://<cognodb-host>:<port>
COGNODB_USERNAME=<username>
COGNODB_PASSWORD=<password>

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>

MEMGRAPH_URI=bolt://localhost:7688
MEMGRAPH_USERNAME=
MEMGRAPH_PASSWORD=

FALKORDB_HOST=localhost
FALKORDB_PORT=6379

Replace the placeholder values with the appropriate local or cloud configuration.

Data Ingestion

The Wiki-Vote dataset is loaded into CognoDB using batches of 1,000 relationships.

Run:

python load_data.py

The ingestion benchmark records:

Total nodes
Total relationships
Batch size
Total insertion time
Relationship ingestion throughput
CognoDB Ingestion Result
Metric	Result
Nodes	7,115
Relationships	103,689
Batch Size	1,000
Insertion Time	294.868 seconds
Throughput	351.65 relationships/sec

Result file:

results/cognodb_ingestion.csv
Query Benchmark

The benchmark evaluates the following graph operations.

1. Point Lookup

Find a user by its ID.

2. Filtered / Indexed Lookup

Find a user using the User.id property and the database's available indexing mechanism.

3. 1-Hop Traversal

Traverse one VOTED_FOR relationship.

4. 2-Hop Traversal

Traverse two consecutive VOTED_FOR relationships.

5. 3-Hop Traversal

Traverse three consecutive VOTED_FOR relationships.

6. Aggregation

Identify users with the highest number of outgoing relationships.

For the latency benchmarks, repeated executions are performed and the following metrics are reported:

p50 latency
p95 latency

A warm-up phase is performed before measured query executions.

CognoDB Benchmark

Run:

python cognodb_benchmark.py

Results are saved to:

results/cognodb_results.csv

CognoDB processed the complete Wiki-Vote graph:

Nodes: 7115
Relationships: 103689
CognoDB Query Results
Metric	p50 (ms)	p95 (ms)
1-Hop Traversal	264.689	409.022
2-Hop Traversal	246.465	397.525
3-Hop Traversal	329.279	784.688
Point Lookup	270.538	726.402
Filtered Lookup	256.037	697.896
Aggregation	369.197	742.751
Mixed Read/Write Benchmark

A mixed workload benchmark is included to evaluate concurrent graph operations.

The workload contains:

Point lookups
Traversals
Aggregations
Relationship writes

The benchmark tests:

1 concurrent client
4 concurrent clients
8 concurrent clients

Run:

python mixed_benchmark.py
CognoDB Mixed Workload Results
Clients	Operations	Completed	Failed	Duration (s)	Throughput (ops/sec)
1	20	20	0	6.813	2.94
4	80	80	0	8.267	9.68
8	160	160	0	8.724	18.34

Result file:

results/cognodb_mixed_workload.csv

All tested mixed-workload operations completed successfully with 0 failures.

Benchmark Comparison

All databases were evaluated using the same logical graph size:

7,115 nodes
103,689 relationships

The final comparison is stored in:

results/final_comparison.csv
Query Latency Comparison
Database	1-Hop p50	2-Hop p50	3-Hop p50	Point Lookup p50	Filtered Lookup p50	Aggregation p50
CognoDB	264.689	246.465	329.279	270.538	256.037	369.197
Neo4j	20.358	19.021	11.157	10.178	8.363	38.766
Memgraph	6.769	6.038	5.717	4.154	4.101	41.957
FalkorDB	2.721	2.447	2.991	2.252	2.285	61.421
Kùzu	1.807	5.541	9.842	0.852	0.916	20.159

All values are p50 client-observed latency in milliseconds from the recorded benchmark run.

p95 Latency Comparison
Database	1-Hop p95	2-Hop p95	3-Hop p95	Point Lookup p95	Filtered Lookup p95	Aggregation p95
CognoDB	409.022	397.525	784.688	726.402	697.896	742.751
Neo4j	28.793	25.486	127.193	13.653	9.690	65.853
Memgraph	14.291	14.442	50.525	5.129	4.840	57.603
FalkorDB	3.218	3.109	3.905	2.652	2.528	71.004
Kùzu	2.417	7.413	12.836	1.169	1.183	22.608
Observed Results
Point Lookup

Kùzu recorded the lowest measured point-lookup latency, followed by FalkorDB, Memgraph, Neo4j, and CognoDB.

Filtered Lookup

Kùzu recorded the lowest measured filtered-lookup latency, followed by FalkorDB, Memgraph, Neo4j, and CognoDB.

Traversal

Kùzu recorded the lowest measured 1-hop latency.

FalkorDB recorded the lowest measured 2-hop and 3-hop traversal latency.

Aggregation

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