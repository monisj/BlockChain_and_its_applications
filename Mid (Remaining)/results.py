import pandas as pd

# Load performance metrics
df = pd.read_csv("Mid (Remaining)\\performance_metrics_threaded.csv")

# Filter only Round-1 and Round-2
df_filtered = df[df['Round'].isin(['Round-1', 'Round-2'])]

# Compute average per Node and Round
summary = df_filtered.groupby(['Node', 'Round']).mean(numeric_only=True).reset_index()

# Pivot to get a side-by-side comparison
access_table = summary.pivot(index='Node', columns='Round', values='Access Time (ms)')
response_table = summary.pivot(index='Node', columns='Round', values='Response Time (ms)')

# Merge both tables
final_summary = pd.concat([access_table, response_table], axis=1)
final_summary.columns = ['Access Time - Round 1', 'Access Time - Round 2', 'Response Time - Round 1', 'Response Time - Round 2']

# Round for display
final_summary = final_summary.round(2)

# Display the comparison table
print("\n📋 Comparison Table (100 vs 200 Requests):\n")
print(final_summary)
