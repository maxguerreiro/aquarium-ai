import gymnasium as gym
import numpy as np

from gymnasium import spaces
from stable_baselines3 import PPO

from aquarium import Aquarium


class FishEnv(gym.Env):

    def __init__(self):

        super().__init__()

        self.width = 1000
        self.height = 700

        # Original aquarium, unchanged
        self.aquarium = Aquarium(
            self.width,
            self.height,
            fish_count=10
        )

        # Load the trained shark V1
        self.shark_model = PPO.load("shark_ppo_model")

        # The fish chooses a movement direction
        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(2,),
            dtype=np.float32
        )

        # Fish observation: 6 normalized values
        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(6,),
            dtype=np.float32
        )

        self.controlled_fish = None

        self.current_step = 0
        self.max_steps = 1800

    def reset(self, seed=None, options=None):

        super().reset(seed=seed)

        # Reset aquarium using the same seed
        self.aquarium.reset(seed=seed)

        self.current_step = 0

        # Select the first fish as the training agent
        self.controlled_fish = self.aquarium.fishes[0]

        observation = self.controlled_fish.get_observation(
            self.aquarium.shark,
            self.width,
            self.height
        )

        return np.array(
            observation,
            dtype=np.float32
        ), {} 