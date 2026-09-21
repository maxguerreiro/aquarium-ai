from gymnasium.utils.env_checker import check_env

from aquarium_ai.aquarium_env_v2 import AquariumEnvV2


env = AquariumEnvV2()

check_env(
    env,
    skip_render_check=True
)

observation, info = env.reset(seed=42)

print("Observação V2:", observation)

print(
    "Quantidade de valores:",
    len(observation)
)

env.close()
