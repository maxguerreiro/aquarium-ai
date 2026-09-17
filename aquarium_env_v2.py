import numpy as np

from gymnasium import spaces

from aquarium_env import AquariumEnv


class AquariumEnvV2(AquariumEnv):

    def __init__(self):

        super().__init__()

        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(8,),
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):

        super().reset(seed=seed, options=options)

        observation = self.aquarium.get_observation_v2()

        return (
            np.array(observation, dtype=np.float32),
            {}
        )

    def step(self, action):

        observation, reward, terminated, truncated, info = (
            super().step(action)
        )

        observation = self.aquarium.get_observation_v2()

        return (
            np.array(observation, dtype=np.float32),
            reward,
            terminated,
            truncated,
            info
        )