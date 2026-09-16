import random
import pygame

from aquarium import Aquarium


pygame.init()

aquarium = Aquarium(1000, 700, 10)

total_reward = 0

for i in range(1800):

    action = pygame.Vector2(
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )

    observation, reward, done = aquarium.step(action)

    total_reward += reward

    if done:
        break

print("Episódio finalizado!")
print(f"Passos executados: {aquarium.current_step}")
print(f"Peixes comidos: {aquarium.score}")
print(f"Recompensa total: {total_reward:.4f}")

pygame.quit()