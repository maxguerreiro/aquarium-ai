from stable_baselines3 import PPO

from aquarium_env import AquariumEnv

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
model.save("shark_ppo_model")

env.close()

print("Treinamento concluído e modelo salvo como 'shark_ppo_model.zip'")