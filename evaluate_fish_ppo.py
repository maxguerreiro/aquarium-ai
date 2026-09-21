"""Compare a trained fish PPO against a random fish."""

import statistics

from stable_baselines3 import PPO
from fish_env import FishEnv


EPISODES = 30
MODEL_PATH = "fish_ppo_model"


def evaluate(env, model=None):

    survival_steps = []
    rewards = []
    captures = 0
    completed = 0

    for episode in range(EPISODES):

        observation, _ = env.reset(seed=1000 + episode)

        total_reward = 0.0
        terminated = False
        truncated = False

        while not (terminated or truncated):

            if model is None:
                action = env.action_space.sample()
            else:
                action, _ = model.predict(
                    observation,
                    deterministic=True
                )

            observation, reward, terminated, truncated, info = env.step(action)

            total_reward += reward

        survival_steps.append(env.current_step)
        rewards.append(total_reward)

        if info["controlled_fish_captured"]:
            captures += 1

        if truncated and not terminated:
            completed += 1

    return {
        "survival": statistics.mean(survival_steps),
        "reward": statistics.mean(rewards),
        "captures": captures,
        "completed": completed
    }


def main():

    env = FishEnv()

    model = PPO.load(MODEL_PATH)

    print("Avaliando peixe aleatório...")
    random_results = evaluate(env)

    print("Avaliando peixe PPO...")
    ppo_results = evaluate(env, model)

    print("\n===== COMPARAÇÃO =====")

    print(
        f"Aleatório | Sobrevivência: "
        f"{random_results['survival']:.1f} | "
        f"Recompensa: {random_results['reward']:.2f} | "
        f"Capturas: {random_results['captures']} | "
        f"Episódios completos: {random_results['completed']}"
    )

    print(
        f"PPO       | Sobrevivência: "
        f"{ppo_results['survival']:.1f} | "
        f"Recompensa: {ppo_results['reward']:.2f} | "
        f"Capturas: {ppo_results['captures']} | "
        f"Episódios completos: {ppo_results['completed']}"
    )

    env.close()


if __name__ == "__main__":
    main()