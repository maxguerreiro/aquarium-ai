import math
import statistics

import pygame

from stable_baselines3 import PPO
from aquarium_env import AquariumEnv


env = AquariumEnv()

model = PPO.load("shark_ppo_model")

observation, info = env.reset(seed=42)

angles = []

terminated = False
truncated = False

while not (terminated or truncated):

    # Action chosen by the neural network
    action, _ = model.predict(
        observation,
        deterministic=True
    )

    ppo_direction = pygame.Vector2(
        float(action[0]),
        float(action[1])
    )

    # Action chosen by our programmed controller
    hunt_direction = env.aquarium.shark.hunt(
        env.aquarium.fishes
    )

    # Compare directions
    if (
        ppo_direction.length_squared() > 0
        and hunt_direction.length_squared() > 0
    ):

        angle = ppo_direction.angle_to(
            hunt_direction
        )

        angle = abs(angle)

        angle = min(angle, 360 - angle)

        angles.append(angle)

    # Only PPO controls the shark
    observation, reward, terminated, truncated, info = env.step(
        action
    )


print("\n===== ANÁLISE DA POLÍTICA =====")

print(f"Capturas: {info['score']}")

print(
    f"Desvio angular médio: "
    f"{statistics.mean(angles):.2f}°"
)

print(
    f"Desvio angular máximo: "
    f"{max(angles):.2f}°"
)

print(
    f"Desvio angular mínimo: "
    f"{min(angles):.2f}°"
)

total = len(angles)

within_15 = sum(angle <= 15 for angle in angles)
within_30 = sum(angle <= 30 for angle in angles)
within_45 = sum(angle <= 45 for angle in angles)

print("\n===== DISTRIBUIÇÃO DOS DESVIOS =====")

print(
    f"Até 15°: {within_15 / total * 100:.2f}%"
)

print(
    f"Até 30°: {within_30 / total * 100:.2f}%"
)

print(
    f"Até 45°: {within_45 / total * 100:.2f}%"
)

env.close()