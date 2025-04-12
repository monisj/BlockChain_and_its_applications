import pandas as pd
from toll_env import TollEnv
from stable_baselines3 import PPO

env = TollEnv(num_booths=5, max_steps=100)
model = PPO.load("ppo_toll_pricing")

obs, _ = env.reset()
toll_log = []

for step in range(env.max_steps):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, _ = env.step(action)

    # Extract current toll values
    current_tolls = obs[:, 2].tolist()
    toll_log.append([step] + current_tolls)

    if terminated:
        break

# Save to CSV
columns = ["step"] + [f"Booth{i+1}" for i in range(env.num_booths)]
df = pd.DataFrame(toll_log, columns=columns)
df.to_csv("toll_log.csv", index=False)
print("✅ Toll log saved to toll_log.csv")
