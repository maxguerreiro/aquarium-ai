"""Visualize ten PPO-controlled fish against the frozen Shark V1 policy."""

import numpy as np
import pygame
from stable_baselines3 import PPO

from aquarium import Aquarium


WIDTH = 1000
HEIGHT = 700
FPS = 60
FISH_COUNT = 10
BACKGROUND = (36, 59, 83)  # #243b53


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aquarium AI - Shark V1 vs All Fish PPO")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    aquarium = Aquarium(WIDTH, HEIGHT, fish_count=FISH_COUNT)

    # Load each frozen policy once, before the simulation loop.
    shark_model = PPO.load("shark_ppo_model")
    fish_model = PPO.load("fish_ppo_model")

    aquarium.reset(seed=42)
    episode = 1
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        # Use a snapshot so fish added by collision respawns are never updated
        # until the next frame.
        fishes_this_frame = list(aquarium.fishes)
        for fish in fishes_this_frame:
            observation = np.asarray(
                fish.get_observation(aquarium.shark, WIDTH, HEIGHT),
                dtype=np.float32,
            )
            action, _ = fish_model.predict(observation, deterministic=True)
            fish.move(
                (float(action[0]), float(action[1])),
                1 / FPS,
                WIDTH,
                HEIGHT,
            )

        # Preserve the six-value V1 shark observation and update order.
        shark_observation = np.asarray(
            aquarium.get_observation(), dtype=np.float32
        )
        shark_action, _ = shark_model.predict(
            shark_observation, deterministic=True
        )
        aquarium.shark.move(
            (float(shark_action[0]), float(shark_action[1])),
            1 / FPS,
            WIDTH,
            HEIGHT,
        )

        for fish in aquarium.fishes[:]:
            if aquarium.shark.collide_with(fish):
                aquarium.fishes.remove(fish)
                aquarium.score += 1
                aquarium.fishes.append(aquarium.create_random_fish())

        aquarium.current_step += 1

        screen.fill(BACKGROUND)
        aquarium.draw(screen)

        score_text = font.render(
            f"Capturas: {aquarium.score}", True, (255, 255, 255)
        )
        episode_text = font.render(
            f"Episódio: {episode}", True, (255, 255, 255)
        )
        screen.blit(score_text, (20, 20))
        screen.blit(episode_text, (20, 50))
        pygame.display.flip()

        if aquarium.is_done():
            print(
                f"Episódio {episode} finalizado | "
                f"Capturas: {aquarium.score}"
            )
            episode += 1
            aquarium.reset()

    pygame.quit()


if __name__ == "__main__":
    main()
