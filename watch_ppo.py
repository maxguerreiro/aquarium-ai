import pygame
import numpy as np

from stable_baselines3 import PPO
from aquarium_env import AquariumEnv


pygame.init()

WIDTH, HEIGHT = 1000, 700
WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aquarium AI - PPO")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Create environment
env = AquariumEnv()

# Load trained model
model = PPO.load("shark_ppo_model")

# Initial observation
observation, info = env.reset(seed=42)

running = True

while running:

    clock.tick(60)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Neural network chooses the action
    action, _ = model.predict(
        observation,
        deterministic=True
    )

    # Execute action
    observation, reward, terminated, truncated, info = env.step(
        action
    )

    # Reset episode
    if terminated or truncated:

        print(
            f"Episódio finalizado! "
            f"Capturas: {info['score']}"
        )

        observation, info = env.reset()

    # Render
    screen.fill((20, 100, 150))

    env.aquarium.draw(screen)

    # Score
    score_text = font.render(
        f"Peixes comidos: {env.aquarium.score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (20, 20))

    pygame.display.flip()


env.close()
pygame.quit()