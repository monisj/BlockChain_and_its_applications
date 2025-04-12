import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Load blockchain ledger
def load_ledger(filename="blockchain_log.json"):
    try:
        with open(filename, "r") as f:
            return pd.DataFrame(json.load(f))
    except:
        return pd.DataFrame(columns=["timestamp", "node", "accuracy", "tokens"])

# Load toll data (optional: simulated output)
def load_toll_logs(filename="toll_log.csv"):
    try:
        df = pd.read_csv(filename)
        return df
    except:
        return pd.DataFrame()

st.set_page_config(page_title="Smart Toll Dashboard", layout="wide")
st.title("🚦 Federated Toll Dashboard")

# Ledger View
st.subheader("📜 Federated Learning Contribution Ledger")
ledger_df = load_ledger()
if not ledger_df.empty:
    st.dataframe(ledger_df.sort_values("timestamp", ascending=False))
    
    # Token Distribution
    tokens = ledger_df.groupby("node")["tokens"].sum().sort_values(ascending=False)
    st.subheader("💰 Token Distribution")
    st.bar_chart(tokens)
else:
    st.warning("No ledger data found.")

# Toll Behavior View (optional logs from env)
st.subheader("📈 Tolling Behavior (Simulated)")

toll_data = load_toll_logs()
if not toll_data.empty:
    booths = toll_data.columns[1:]  # skip 'step' column
    step = toll_data["step"]
    for b in booths:
        plt.plot(step, toll_data[b], label=b)
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Toll Price")
    plt.title("Toll Price Over Time")
    st.pyplot(plt.gcf())
    plt.clf()
else:
    st.info("No toll simulation data available (toll_log.csv not found).")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit.")
