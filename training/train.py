from pathlib import Path

from stable_baselines3 import PPO

from aquarium_ai.aquarium_env import AquariumEnv


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "shark_ppo_model"

#Create training environment
env = AquariumEnv()

#Create PPO model
model = PPO("MlpPolicy", 
            env, 
            verbose=1, 
            seed = 42
        )

#Train agent
model.learn(total_timesteps=100_000)

#Save model
model.save(MODEL_PATH)

env.close()

print("Treinamento concluído e modelo salvo como 'shark_ppo_model.zip'")
