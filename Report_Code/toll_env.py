import gymnasium as gym
from gymnasium import spaces
import numpy as np

class TollEnv(gym.Env):
    def __init__(self, num_booths=5, max_steps=100):
        super(TollEnv, self).__init__()
        self.num_booths = num_booths
        self.max_steps = max_steps
        self.current_step = 0

        # Action: toll per booth [0, 1, 2] = low, medium, high
        self.action_space = spaces.MultiDiscrete([3] * self.num_booths)

        # Observation: congestion level (0-1), vehicle count (0-100), prev toll
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.num_booths, 3), dtype=np.float32)

        self.reset()

    def step(self, action):
        tolls = action / 2.0  # normalize toll (0.0 - 1.0)
        vehicle_counts = self.state[:, 1]
        congestion = np.clip(1 - tolls + 0.2 * np.random.randn(self.num_booths), 0, 1)
        travel_time = congestion * (1 + vehicle_counts / 100)

        # Reward: negative of total travel time + mild reward for collected toll
        reward = -np.sum(travel_time) + np.sum(tolls * vehicle_counts * 0.05)

        self.current_step += 1
        done = self.current_step >= self.max_steps

        next_vehicle_counts = np.clip(vehicle_counts + np.random.randint(-10, 10, size=self.num_booths), 10, 100)
        next_vehicle_counts_norm = next_vehicle_counts / 100.0
        # Next state
        self.state = np.stack([
            congestion,
             next_vehicle_counts_norm,
            tolls
        ], axis=1)

        terminated = self.current_step >= self.max_steps
        truncated = False  # unless you plan to use time-limits or early stops

        return self.state.astype(np.float32), reward, terminated, truncated, {}


    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        self.current_step = 0
        congestion = np.random.uniform(0.3, 0.7, size=self.num_booths)
        vehicle_count = np.random.randint(20, 80, size=self.num_booths)
        prev_toll = np.zeros(self.num_booths)

        self.state = np.stack([congestion, vehicle_count / 100.0, prev_toll], axis=1).astype(np.float32)
        return self.state, {}  # ← must return (obs, info)


    def render(self, mode='human'):
        print(f"Step {self.current_step}: Tolls {self.state[:,2]}")
