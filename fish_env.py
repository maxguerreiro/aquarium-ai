"""Gymnasium environment for training one fish against the frozen shark V1."""

import math

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from stable_baselines3 import PPO

from aquarium import Aquarium


class FishEnv(gym.Env):
    """Train a fish to survive while ``shark_ppo_model.zip`` controls the shark.

    This class deliberately does not change :class:`Aquarium` or
    :class:`AquariumEnv`, which remain the original V1 shark environment.
    """

    metadata = {"render_modes": []}

    def __init__(self, shark_model_path="shark_ppo_model"):
        super().__init__()

        self.width = 1000
        self.height = 700
        self.dt = 1 / 60
        self.max_steps = 1800
        self.aquarium = Aquarium(self.width, self.height, fish_count=10)

        # The model is loaded for inference only; FishEnv never calls learn().
        self.shark_model = PPO.load(shark_model_path)

        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(2,), dtype=np.float32
        )
        # Fish position, relative shark position and fish direction.
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(6,), dtype=np.float32
        )

        self.controlled_fish = None
        self.current_step = 0

    def _fish_observation(self):
        return np.array(
            self.controlled_fish.get_observation(
                self.aquarium.shark, self.width, self.height
            ),
            dtype=np.float32,
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.aquarium.reset(seed=seed)
        self.current_step = 0
        self.controlled_fish = self.aquarium.fishes[0]
        return self._fish_observation(), {}

    def step(self, action):
        if self.controlled_fish is None:
            raise RuntimeError("Execute reset() antes de chamar step().")

        action = np.asarray(action, dtype=np.float32)
        if action.shape != self.action_space.shape:
            raise ValueError("A ação do peixe deve ter exatamente dois valores.")
        action = np.clip(action, self.action_space.low, self.action_space.high)

        shark = self.aquarium.shark
        distance_before = self.controlled_fish.position.distance_to(shark.position)

        # Only the training fish obeys the supplied action. The remaining fish
        # keep the original autonomous movement from the V1 simulation.
        self.controlled_fish.move(action, self.dt, self.width, self.height)
        for fish in self.aquarium.fishes:
            if fish is not self.controlled_fish:
                fish.update(self.dt, self.width, self.height)

        # This is the exact six-value input expected by the frozen V1 model.
        shark_observation = np.asarray(self.aquarium.get_observation(), dtype=np.float32)
        shark_action, _ = self.shark_model.predict(
            shark_observation, deterministic=True
        )
        shark.move(
            (float(shark_action[0]), float(shark_action[1])),
            self.dt,
            self.width,
            self.height,
        )

        controlled_captured = False
        fish_captured = 0
        for fish in self.aquarium.fishes[:]:
            if shark.collide_with(fish):
                if fish is self.controlled_fish:
                    controlled_captured = True
                self.aquarium.fishes.remove(fish)
                self.aquarium.score += 1
                fish_captured += 1
                # Every eaten fish is replaced, preserving the population size.
                self.aquarium.fishes.append(self.aquarium.create_random_fish())

        self.current_step += 1
        self.aquarium.current_step = self.current_step
        terminated = controlled_captured
        truncated = self.current_step >= self.max_steps

        distance_after = self.controlled_fish.position.distance_to(shark.position)
        diagonal = math.hypot(self.width, self.height)

        # Living is the primary objective; separation is a small dense signal.
        if controlled_captured:
            reward = -10.0
        else:
            reward = 0.01 + (distance_after - distance_before) / diagonal

        info = {
            "score": self.aquarium.score,
            "fish_captured": fish_captured,
            "controlled_fish_captured": controlled_captured,
            "distance_to_shark": distance_after,
        }
        return self._fish_observation(), float(reward), terminated, truncated, info
