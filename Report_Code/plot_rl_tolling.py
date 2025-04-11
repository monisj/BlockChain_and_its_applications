import numpy as np
import matplotlib.pyplot as plt
from toll_env import TollEnv
from stable_baselines3 import PPO

# Load environment and trained model
env = TollEnv(num_booths=5, max_steps=100)
model = PPO.load("Report_Code\\ppo_toll_pricing")

# Storage
toll_log = []
congestion_log = []
reward_log = []

obs, _ = env.reset()
total_reward = 0

for _ in range(env.max_steps):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, _ = env.step(action)

    toll_log.append(obs[:, 2].tolist())         # current toll values
    congestion_log.append(obs[:, 0].tolist())   # current congestion
    reward_log.append(reward)
    total_reward += reward

    if terminated:
        break

# Convert logs
toll_log = np.array(toll_log)          # shape: [T, num_booths]
congestion_log = np.array(congestion_log)
reward_log = np.array(reward_log)

# === Plot 1: Toll evolution ===
plt.figure(figsize=(10, 4))
for i in range(env.num_booths):
    plt.plot(toll_log[:, i], label=f"Booth {i+1}")
plt.title("Toll Price per Booth Over Time")
plt.xlabel("Time Step")
plt.ylabel("Toll Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Plot 2: Congestion per booth ===
plt.figure(figsize=(10, 4))
for i in range(env.num_booths):
    plt.plot(congestion_log[:, i], label=f"Booth {i+1}")
plt.title("Congestion Level per Booth Over Time")
plt.xlabel("Time Step")
plt.ylabel("Congestion (0–1)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Plot 3: Reward per step ===
plt.figure(figsize=(10, 4))
plt.plot(reward_log, marker="o", color="teal")
plt.title("Episode Reward Over Time")
plt.xlabel("Time Step")
plt.ylabel("Reward")
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"✅ Total episode reward: {total_reward:.2f}")
