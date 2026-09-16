import random
import statistics

import pygame

from aquarium import Aquarium


EPISODES = 100


def random_controller(aquarium):

    return pygame.Vector2(
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )


def programmed_controller(aquarium):

    return aquarium.shark.hunt(aquarium.fishes)


def evaluate(controller):

    scores = []
    rewards = []

    aquarium = Aquarium(1000, 700, 10)

    for episode in range(EPISODES):

        aquarium.reset()

        total_reward = 0

        while not aquarium.is_done():

            action = controller(aquarium)

            observation, reward, done = aquarium.step(action)

            total_reward += reward

        scores.append(aquarium.score)

        rewards.append(total_reward)

    return {
        "scores": scores,
        "rewards": rewards,
        "average_score": statistics.mean(scores),
        "average_reward": statistics.mean(rewards)
    }


pygame.init()

print("Avaliando controlador aleatório...")

random_results = evaluate(random_controller)

print("Avaliando controlador programado...")

programmed_results = evaluate(programmed_controller)


print("\n===== RESULTADOS =====")

print("\nALEATÓRIO")
print(f"Capturas médias: {random_results['average_score']:.2f}")
print(f"Recompensa média: {random_results['average_reward']:.2f}")

print("\nPROGRAMADO")
print(f"Capturas médias: {programmed_results['average_score']:.2f}")
print(f"Recompensa média: {programmed_results['average_reward']:.2f}")

pygame.quit()