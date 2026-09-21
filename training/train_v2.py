from pathlib import Path

from stable_baselines3 import PPO

from aquarium_ai.aquarium_env_v2 import AquariumEnvV2


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "shark_ppo_model_v2"


# Create the new environment
env = AquariumEnvV2()

# Create a new PPO model
model = PPO(
    policy="MlpPolicy",
    env=env,
    verbose=1,
    seed=42
)

# Train the model
model.learn(
    total_timesteps=100_000
)

# Save without overwriting V1
model.save(MODEL_PATH)

env.close()

print("\nTreinamento V2 concluído!")
print("Modelo salvo: shark_ppo_model_v2.zip")
