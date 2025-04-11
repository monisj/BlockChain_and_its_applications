from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from toll_env import TollEnv

env = TollEnv(num_booths=5)
check_env(env, warn=True)

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./toll_rl_tensorboard/")
model.learn(total_timesteps=20000)

model.save("ppo_toll_pricing")
print("RL toll pricing model saved.")
