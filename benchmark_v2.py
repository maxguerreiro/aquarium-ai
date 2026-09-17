import statistics

import numpy as np
import pygame

from stable_baselines3 import PPO

from aquarium_env import AquariumEnv
from aquarium_env_v2 import AquariumEnvV2


EPISODES = 100
BASE_SEED = 1000


model_v1 = PPO.load("shark_ppo_model")
model_v2 = PPO.load("shark_ppo_model_v2")


def evaluate(controller, seed):

    if controller == "ppo_v2":
        env = AquariumEnvV2()
    else:
        env = AquariumEnv()

    observation, info = env.reset(seed=seed)

    total_reward = 0.0

    terminated = False
    truncated = False

    while not (terminated or truncated):

        if controller == "ppo_v1":

            action, _ = model_v1.predict(
                observation,
                deterministic=True
            )

        elif controller == "ppo_v2":

            action, _ = model_v2.predict(
                observation,
                deterministic=True
            )

        elif controller == "hunt":

            direction = env.aquarium.shark.hunt(
                env.aquarium.fishes
            )

            action = np.array(
                [direction.x, direction.y],
                dtype=np.float32
            )

        elif controller == "random":

            action = env.action_space.sample()

        observation, reward, terminated, truncated, info = (
            env.step(action)
        )

        total_reward += reward

    captures = info["score"]

    env.close()

    return captures, total_reward


controllers = [
    "random",
    "hunt",
    "ppo_v1",
    "ppo_v2"
]

results = {
    name: {
        "captures": [],
        "rewards": []
    }
    for name in controllers
}


for episode in range(EPISODES):

    seed = BASE_SEED + episode

    for controller in controllers:

        captures, reward = evaluate(
            controller,
            seed
        )

        results[controller]["captures"].append(
            captures
        )

        results[controller]["rewards"].append(
            reward
        )

    print(
        f"Episódio {episode + 1:03d}/{EPISODES} concluído"
    )


print("\n========== RESULTADOS ==========")

for controller in controllers:

    captures = results[controller]["captures"]
    rewards = results[controller]["rewards"]

    print(f"\n{controller.upper()}")

    print(
        f"Capturas médias: "
        f"{statistics.mean(captures):.2f}"
    )

    print(
        f"Recompensa média: "
        f"{statistics.mean(rewards):.2f}"
    )

    print(
        f"Desvio padrão das capturas: "
        f"{statistics.stdev(captures):.2f}"
    )

    print(
        f"Menor número de capturas: {min(captures)}"
    )

    print(
        f"Maior número de capturas: {max(captures)}"
    )