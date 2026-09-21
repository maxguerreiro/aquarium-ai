import numpy as np
from gymnasium.utils.env_checker import check_env

from fish_env import FishEnv


env = FishEnv()

# The complete environment must satisfy Gymnasium's API, not only reset().
check_env(env, skip_render_check=True)

observation, info = env.reset(seed=42)
assert observation.shape == (6,)
assert env.observation_space.contains(observation)
assert env.controlled_fish is env.aquarium.fishes[0]

observation, reward, terminated, truncated, info = env.step(
    np.array([1.0, 0.0], dtype=np.float32)
)
assert observation.shape == (6,)
assert isinstance(reward, float)
assert not terminated
assert not truncated
assert info["controlled_fish_captured"] is False

# A non-controlled fish captured by the shark must be replaced.
victim = env.aquarium.fishes[1]
victim.position = env.aquarium.shark.position.copy()
victim.speed = 0
population_before = len(env.aquarium.fishes)
_, _, _, _, info = env.step(np.array([0.0, 0.0], dtype=np.float32))
assert info["fish_captured"] >= 1
assert len(env.aquarium.fishes) == population_before

# Capture of the controlled fish ends its episode and has a penalty.
env.reset(seed=7)
env.controlled_fish.position = env.aquarium.shark.position.copy()
env.controlled_fish.speed = 0
env.aquarium.shark.speed = 0
_, reward, terminated, truncated, info = env.step(
    np.array([0.0, 0.0], dtype=np.float32)
)
assert terminated
assert not truncated
assert reward < -9.0
assert info["controlled_fish_captured"] is True
assert len(env.aquarium.fishes) == env.aquarium.fish_count

env.close()
print("FishEnv validated successfully!")
