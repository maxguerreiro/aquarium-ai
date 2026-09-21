import statistics
from pathlib import Path

from stable_baselines3 import PPO
from aquarium_ai.aquarium_env import AquariumEnv


EPISODES = 100
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "shark_ppo_model.zip"

env = AquariumEnv()

model = PPO.load(MODEL_PATH, env=env)

scores = []
rewards = []

for episode in range(EPISODES):

    observation, info = env.reset(
        seed=1000 + episode
    )

    total_reward = 0.0

    terminated = False
    truncated = False

    while not (terminated or truncated):

        action, _ = model.predict(
            observation,
            deterministic=True
        )

        observation, reward, terminated, truncated, info = env.step(
            action
        )

        total_reward += reward

    scores.append(info["score"])
    rewards.append(total_reward)

    print(
        f"Episódio {episode + 1:03d} | "
        f"Capturas: {info['score']:02d} | "
        f"Recompensa: {total_reward:.2f}"
    )

print("\n===== RESULTADOS PPO =====")

print(
    f"Capturas médias: {statistics.mean(scores):.2f}"
)

print(
    f"Recompensa média: {statistics.mean(rewards):.2f}"
)

print(
    f"Menor número de capturas: {min(scores)}"
)

print(
    f"Maior número de capturas: {max(scores)}"
)

env.close()
