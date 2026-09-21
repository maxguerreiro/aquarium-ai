from gymnasium.utils.env_checker import check_env

from aquarium_ai.aquarium_env import AquariumEnv


env = AquariumEnv()

check_env(env, skip_render_check=True)

print("Ambiente validado com sucesso!")

env.close()
