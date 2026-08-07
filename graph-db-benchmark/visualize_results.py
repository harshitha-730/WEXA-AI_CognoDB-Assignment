import pandas as pd
import matplotlib.pyplot as plt
import os


# Load final comparison
df = pd.read_csv(
    "results/final_comparison.csv",
    encoding="latin1"
)


# Create output folder
os.makedirs(
    "results/plots",
    exist_ok=True
)



# -------------------------------
# Traversal comparison
# -------------------------------

plt.figure(figsize=(10,6))

for col in [
    "traversal_1hop_p50_ms",
    "traversal_2hop_p50_ms",
    "traversal_3hop_p50_ms"
]:
    plt.plot(
        df["Database"],
        df[col],
        marker="o",
        label=col.replace("_p50_ms","")
    )


plt.xlabel("Database")
plt.ylabel("Latency (ms)")
plt.title("Traversal Performance Comparison")
plt.legend()
plt.grid(True)

plt.savefig(
    "results/plots/traversal_comparison.png",
    bbox_inches="tight"
)

plt.close()



# -------------------------------
# Lookup comparison
# -------------------------------

plt.figure(figsize=(10,6))

x = df["Database"]

plt.plot(
    x,
    df["point_lookup_p50_ms"],
    marker="o",
    label="Point Lookup"
)

plt.plot(
    x,
    df["filtered_lookup_p50_ms"],
    marker="o",
    label="Filtered Lookup"
)


plt.xlabel("Database")
plt.ylabel("Latency (ms)")
plt.title("Lookup Performance Comparison")
plt.legend()
plt.grid(True)

plt.savefig(
    "results/plots/lookup_comparison.png",
    bbox_inches="tight"
)

plt.close()



# -------------------------------
# Aggregation comparison
# -------------------------------

plt.figure(figsize=(10,6))


plt.bar(
    df["Database"],
    df["aggregation_p50_ms"]
)


plt.xlabel("Database")
plt.ylabel("Latency (ms)")
plt.title("Aggregation Query Performance")


plt.savefig(
    "results/plots/aggregation_comparison.png",
    bbox_inches="tight"
)

plt.close()



print("Charts generated successfully!")
print("Location: results/plots/")