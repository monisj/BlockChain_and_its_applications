import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_traffic_data(num_segments=10, days=7, interval_minutes=15):
    data = []
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    end_time = start_time + timedelta(days=days)
    time_points = int((24 * 60 / interval_minutes) * days)

    for seg_id in range(1, num_segments + 1):
        timestamp = start_time
        for _ in range(time_points):
            vehicle_count = np.random.poisson(lam=random.randint(10, 50))
            avg_speed = np.clip(np.random.normal(loc=60 - vehicle_count * 0.5, scale=5), 5, 120)
            data.append([timestamp, seg_id, vehicle_count, avg_speed])
            timestamp += timedelta(minutes=interval_minutes)

    df = pd.DataFrame(data, columns=["timestamp", "segment_id", "vehicle_count", "avg_speed"])
    return df

# Generate and save the data
df = generate_traffic_data()
df.to_csv("synthetic_traffic_data.csv", index=False)
print("Synthetic traffic data generated and saved to 'synthetic_traffic_data.csv'")
