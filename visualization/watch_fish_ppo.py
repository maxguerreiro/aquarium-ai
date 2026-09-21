import pygame
from pathlib import Path

from stable_baselines3 import PPO
from aquarium_ai.fish_env import FishEnv


# Window settings
WIDTH = 1000
HEIGHT = 700
FPS = 60

BACKGROUND = (36, 59, 83)
HIGHLIGHT = (255, 255, 255)


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(
        "Aquarium AI - Shark V1 vs Fish PPO"
    )

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 30)

    # Create environment
    env = FishEnv()

    # Load trained fish
    model_path = Path(__file__).resolve().parents[1] / "models" / "fish_ppo_model.zip"
    fish_model = PPO.load(model_path)

    # Reset environment
    observation, info = env.reset(seed=42)

    running = True
    episode = 1

    while running:

        clock.tick(FPS)

        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # Fish chooses action
        action, _ = fish_model.predict(
            observation,
            deterministic=True
        )

        # Execute environment step
        observation, reward, terminated, truncated, info = env.step(
            action
        )

        # Render background
        screen.fill(BACKGROUND)

        # Draw aquarium
        env.aquarium.draw(screen)

        # Highlight trained fish
        if not terminated:

            fish = env.controlled_fish

            pygame.draw.circle(
                screen,
                HIGHLIGHT,
                (
                    int(fish.position.x),
                    int(fish.position.y)
                ),
                fish.radius + 8,
                2
            )

        # HUD
        score_text = font.render(
            f"Capturas: {env.aquarium.score}",
            True,
            HIGHLIGHT
        )

        episode_text = font.render(
            f"Episodio: {episode}",
            True,
            HIGHLIGHT
        )

        survival_text = font.render(
            f"Sobrevivencia: {env.current_step}",
            True,
            HIGHLIGHT
        )

        screen.blit(score_text, (20, 20))
        screen.blit(episode_text, (20, 50))
        screen.blit(survival_text, (20, 80))

        pygame.display.flip()

        # Reset episode
        if terminated or truncated:

            print(
                f"Episodio {episode} finalizado | "
                f"Sobrevivencia: {env.current_step} passos | "
                f"Capturado: {info['controlled_fish_captured']}"
            )

            episode += 1

            observation, info = env.reset()

    env.close()

    pygame.quit()


if __name__ == "__main__":
    main()
