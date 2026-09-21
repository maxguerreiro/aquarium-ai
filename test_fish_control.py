import pygame

from fish import Fish


pygame.init()

# Create a fish at the center of the aquarium
fish = Fish(
    x=500,
    y=350,
    speed=120,
    direction=(1, 0)
)

WIDTH = 1000
HEIGHT = 700

DT = 1 / 60

print("Initial position:", fish.position)

# Move upward for 60 frames (1 second)
for _ in range(60):

    fish.move(
        action=(0, -1),
        dt=DT,
        width=WIDTH,
        height=HEIGHT
    )

print("Position after moving up:", fish.position)
print("Final direction:", fish.direction)

# Test aquarium boundaries
for _ in range(1000):

    fish.move(
        action=(-1, 0),
        dt=DT,
        width=WIDTH,
        height=HEIGHT
    )

print("Position after reaching left wall:", fish.position)

assert abs(fish.position.x - fish.radius) < 0.001

assert abs(fish.position.y - 230) < 0.001

print("All tests passed!")

pygame.quit()