import pygame

from aquarium_ai.fish import Fish
from aquarium_ai.shark import Shark


pygame.init()

fish = Fish(
    x=500,
    y=350,
    speed=120,
    direction=(1, 0)
)

# We only need the shark's position for this test.
# Use a lightweight object to avoid depending on
# Shark's constructor.
class DummyShark:

    def __init__(self):
        self.position = pygame.Vector2(750, 350)


shark = DummyShark()

observation = fish.get_observation(
    shark=shark,
    width=1000,
    height=700
)

print("Fish observation:", observation)
print("Observation size:", len(observation))

assert len(observation) == 6

assert abs(observation[0] - 0.5) < 0.0001
assert abs(observation[1] - 0.5) < 0.0001

# Shark is 250 pixels to the right.
assert abs(observation[2] - 0.25) < 0.0001
assert abs(observation[3]) < 0.0001

print("All observation tests passed!")

pygame.quit()
