import csv
import os


def save_metrics(results, filename="results/benchmark_results.csv"):

    os.makedirs("results", exist_ok=True)

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Operation", "Execution Time (ms)"])

        for operation, value in results:
            writer.writerow([operation, value])
            