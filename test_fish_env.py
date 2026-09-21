from fish_env import FishEnv


env = FishEnv()

observation, info = env.reset(seed=42)

print("Observation:", observation)

print("Observation shape:", observation.shape)

print("Action space:", env.action_space)

print("Observation space:", env.observation_space)

print(
    "Controlled fish:",
    env.controlled_fish.position
)

print(
    "Shark:",
    env.aquarium.shark.position
)

assert observation.shape == (6,)

assert env.controlled_fish is env.aquarium.fishes[0]

print("Fish environment reset passed!")

env.close()