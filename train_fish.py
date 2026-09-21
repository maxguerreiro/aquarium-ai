"""Train a fish PPO policy against the frozen shark V1."""

from stable_baselines3 import PPO

from fish_env import FishEnv


TOTAL_TIMESTEPS = 100_000
MODEL_PATH = "fish_ppo_model"


def main():
    env = FishEnv()
    model = PPO("MlpPolicy", env, verbose=1, seed=42)
    model.learn(total_timesteps=TOTAL_TIMESTEPS)
    model.save(MODEL_PATH)
    env.close()
    print(f"Treinamento concluído. Modelo salvo como '{MODEL_PATH}.zip'.")


if __name__ == "__main__":
    main()
