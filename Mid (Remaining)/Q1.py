import threading
import time
import random
import csv
import subprocess
import json

# Configuration
nodes = [
    {"name": "Node A", "chain": "chain_node_a"},
    {"name": "Node B", "chain": "chain_node_b"},
    {"name": "Node C", "chain": "chain_node_c"},
]
vehicle_chain = "chain_vehicle"

rounds = [
    {"name": "Round-1", "delay": 0.6, "requests_per_node": 100},
    {"name": "Round-2", "delay": 0.12, "requests_per_node": 200},
]

# Thread-safe performance log
performance_logs = []
log_lock = threading.Lock()

# Helper function to publish to a MultiChain stream
def publish_to_stream(chain, stream, key, json_data):
    command = [
        "multichain-cli", chain,
        "publish", stream, key, json.dumps({"json": json_data})
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"[{chain}] ✔ Published to {stream}: {key}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[{chain}] ✘ Error publishing to {stream}: {e.stderr.strip()}")
        return None

# Simulate vehicular node response
def vehicular_node_process(request_time):
    processing_delay = random.uniform(0.1, 0.3)
    time.sleep(processing_delay)
    return time.time()

# Simulate request handling for a node
def simulate_node_requests(node_info, delay, num_requests, round_name):
    node_name = node_info["name"]
    chain_name = node_info["chain"]
    stream_name = f"stream_{node_name.replace(' ', '_').lower()}"
    
    for i in range(num_requests):
        time.sleep(delay)
        t1 = time.time()
        request_key = f"{node_name}_{i}"

        # Publish request to node's own chain
        publish_to_stream(
            chain=chain_name,
            stream=stream_name,
            key=request_key,
            json_data={"timestamp": t1}
        )

        # Vehicle processes and publishes to vehicle chain
        t3 = vehicular_node_process(t1)

        publish_to_stream(
            chain=vehicle_chain,
            stream="stream_vehicle",
            key=request_key,
            json_data={
                "from": node_name,
                "request_time": t1,
                "response_time": t3
            }
        )

        # Log performance
        with log_lock:
            performance_logs.append({
                "Node": node_name,
                "Chain": chain_name,
                "Round": round_name,
                "Access Time (ms)": round((t3 - t1) * 1000, 2),
                "Response Time (ms)": round((t3 - t1) * 1000, 2)
            })

# Run one simulation round using threads
def run_round(round_cfg):
    threads = []
    for node_info in nodes:
        t = threading.Thread(
            target=simulate_node_requests,
            args=(node_info, round_cfg["delay"], round_cfg["requests_per_node"], round_cfg["name"])
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Main simulation loop
if __name__ == "__main__":
    for round_cfg in rounds:
        print(f"\n▶ Starting {round_cfg['name']}...")
        run_round(round_cfg)
        print(f"✔ Completed {round_cfg['name']}.")

    # Save results
    csv_filename = "performance_metrics_multichain_threaded.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Node", "Chain", "Round", "Access Time (ms)", "Response Time (ms)"])
        writer.writeheader()
        for entry in performance_logs:
            writer.writerow(entry)

    print(f"\n📁 Results saved to {csv_filename}")
