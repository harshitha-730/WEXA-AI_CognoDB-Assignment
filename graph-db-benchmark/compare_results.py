import pandas as pd
import os


# Input result files
files = {
    "Neo4j": "results/neo4j_results.csv",
    "Memgraph": "results/memgraph_results.csv",
    "FalkorDB": "results/falkordb_results.csv",
    "Kùzu": "results/kuzu_results.csv"
}


all_results = []


for db_name, file_path in files.items():

    # Read CSV with encoding support
    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    # Add database name column
    df.insert(
        0,
        "Database",
        db_name
    )

    # Fix encoding issue for Kùzu
    df["Database"] = df["Database"].replace(
        "KÃ¹zu",
        "Kùzu"
    )

    df["platform"] = df["platform"].replace(
        "KÃ¹zu",
        "Kùzu"
    )

    all_results.append(df)



# Combine all database results
comparison = pd.concat(
    all_results,
    ignore_index=True
)



# Create results folder if missing
os.makedirs(
    "results",
    exist_ok=True
)



# Save final comparison
output_file = "results/final_comparison.csv"

comparison.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)



print("\nFinal Comparison:")
print(comparison.to_string())


print(f"\nSaved: {output_file}")