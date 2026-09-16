import gymnasium as gym
import numpy as np
import pygame

from gymnasium import spaces
from aquarium import Aquarium


class AquariumEnv(gym.Env):

    def __init__(self):

        super().__init__()

        self.aquarium = Aquarium(1000, 700, 10)

        # Two continuous actions: X and Y
        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(2,),
            dtype=np.float32
        )

        # Six numerical observations
        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(6,),
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):

        super().reset(seed=seed)

        observation = self.aquarium.reset(seed=seed)

        return (
            np.array(observation, dtype=np.float32),
            {}
        )

    def step(self, action):

        observation, reward, done = self.aquarium.step(
            pygame.Vector2(
                float(action[0]),
                float(action[1])
            )
        )

        terminated = False
        truncated = done

        info = {
            "score": self.aquarium.score
        }

        return (
            np.array(observation, dtype=np.float32),
            float(reward),
            terminated,
            truncated,
            info
        )