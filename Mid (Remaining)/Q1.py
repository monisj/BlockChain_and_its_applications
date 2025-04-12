import threading
import time
import random
import csv

# Configuration
nodes = ['Node A', 'Node B', 'Node C']
rounds = [
    {"name": "Round-1", "delay": 0.6, "requests_per_node": 100},
    {"name": "Round-2", "delay": 0.12, "requests_per_node": 200},
]

# Simulated blockchain "streams" for each node + vehicle
streams = {
    "stream_node_a": [],
    "stream_node_b": [],
    "stream_node_c": [],
    "stream_vehicle": []
}

# Thread-safe log
performance_logs = []
log_lock = threading.Lock()

# Simulate vehicular node response
def vehicular_node_process(request_time):
    processing_delay = random.uniform(0.1, 0.3)
    time.sleep(processing_delay)
    return time.time()

# Simulate request handling for a node
def simulate_node_requests(node_name, delay, num_requests, round_name):
    stream_name = f"stream_{node_name.replace(' ', '_').lower()}"

    for i in range(num_requests):
        time.sleep(delay)
        t1 = time.time()

        # Simulate writing request to citizen node's chain
        with log_lock:
            streams[stream_name].append({
                "request_id": f"{node_name}_{i}",
                "timestamp": t1
            })

        # Simulate processing and publishing by vehicular node
        t3 = vehicular_node_process(t1)

        with log_lock:
            streams["stream_vehicle"].append({
                "from": node_name,
                "request_id": f"{node_name}_{i}",
                "request_time": t1,
                "response_time": t3
            })

            performance_logs.append({
                "Node": node_name,
                "Chain": stream_name,
                "Round": round_name,
                "Access Time (ms)": round((t3 - t1) * 1000, 2),
                "Response Time (ms)": round((t3 - t1) * 1000, 2)
            })

# Simulate a full round with multiple threads
def run_round(round_cfg):
    threads = []
    for node in nodes:
        t = threading.Thread(
            target=simulate_node_requests,
            args=(node, round_cfg["delay"], round_cfg["requests_per_node"], round_cfg["name"])
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Main simulation
if __name__ == "__main__":
    for round_cfg in rounds:
        print(f"Starting {round_cfg['name']}...")
        run_round(round_cfg)
        print(f"Completed {round_cfg['name']}.\n")

    # Save results to CSV
    csv_filename = "performance_metrics_threaded.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Node", "Chain", "Round", "Access Time (ms)", "Response Time (ms)"])
        writer.writeheader()
        for entry in performance_logs:
            writer.writerow(entry)

    print(f"\nResults saved to {csv_filename}")
