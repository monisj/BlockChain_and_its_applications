import pandas as pd
import matplotlib.pyplot as plt

# Load the simulation data
df = pd.read_csv("Mid (Remaining)\\performance_metrics.csv")

# Group and calculate average
summary = df.groupby(["Node", "Round"]).mean(numeric_only=True).reset_index()

# Set up plotting
rounds = summary["Round"].unique()
nodes = summary["Node"].unique()

# Prepare data
access_data = summary.pivot(index="Round", columns="Node", values="Access Time (ms)")
response_data = summary.pivot(index="Round", columns="Node", values="Response Time (ms)")

# Plot Average Access Time
access_data.plot(kind='bar', figsize=(10, 6))
plt.title("Average Access Time per Node per Round")
plt.ylabel("Access Time (ms)")
plt.xlabel("Round")
plt.xticks(rotation=0)
plt.legend(title="Node")
plt.tight_layout()
plt.grid(True)
plt.show()

# Plot Average Response Time
response_data.plot(kind='bar', figsize=(10, 6))
plt.title("Average Response Time per Node per Round")
plt.ylabel("Response Time (ms)")
plt.xlabel("Round")
plt.xticks(rotation=0)
plt.legend(title="Node")
plt.tight_layout()
plt.grid(True)
plt.show()
