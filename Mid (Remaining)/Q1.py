import asyncio
import random
import time
import csv
from datetime import datetime

# Configuration
nodes = ['Node A', 'Node B', 'Node C']
rounds = [
    {"name": "Round-1", "delay": 0.6, "requests_per_node": 100},
    {"name": "Round-2", "delay": 0.12, "requests_per_node": 200},
]

performance_logs = []

# Simulate vehicular node response time
async def vehicular_node_process(request_time):
    processing_delay = random.uniform(0.1, 0.3)  # Simulate response delay
    await asyncio.sleep(processing_delay)
    response_time = time.time()
    return request_time, response_time

# Simulate one node sending requests
async def simulate_node_requests(node_name, delay, num_requests, round_name):
    for _ in range(num_requests):
        await asyncio.sleep(delay)  # delay between requests
        t1 = time.time()  # request sent
        _, t3 = await vehicular_node_process(t1)  # simulate process and response
        access_time = t3 - t1
        response_time = t3 - t1  # same in this sim, update if t2 included
        performance_logs.append({
            "Node": node_name,
            "Round": round_name,
            "Access Time (ms)": round(access_time * 1000, 2),
            "Response Time (ms)": round(response_time * 1000, 2)
        })

# Simulate a full round
async def simulate_round(round_config):
    delay = round_config["delay"]
    tasks = []
    for node in nodes:
        tasks.append(simulate_node_requests(node, delay, round_config["requests_per_node"], round_config["name"]))
    await asyncio.gather(*tasks)

# Run the simulation
async def run_simulation():
    for round_cfg in rounds:
        print(f"Starting {round_cfg['name']}...")
        await simulate_round(round_cfg)
        print(f"Completed {round_cfg['name']}.\n")

# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("Simulation interrupted.")

    # Save results
    csv_filename = "performance_metrics.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Node", "Round", "Access Time (ms)", "Response Time (ms)"])
        writer.writeheader()
        for entry in performance_logs:
            writer.writerow(entry)

    print(f"\nResults saved to {csv_filename}")
