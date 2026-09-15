import random
import pygame

from fish import Fish


pygame.init()

# Set up the display

WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aquarium AI")

clock = pygame.time.Clock()

# Create fish instances
fishes = [] 

for i in range(10):

    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)

    speed = random.randint(50, 150)

    direction = pygame.Vector2(
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )

    # Ensure the direction is not zero to avoid division by zero
    if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
    else:
            direction = direction.normalize()

    fish = Fish(x, y, speed, direction)

    fishes.append(fish)

running = True

while running:

    dt = clock.tick(60) / 1000  # Amount of seconds between each loop (Delta time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update fish position
    for fish in fishes:
        fish.update(dt, WIDTH, HEIGHT)

    screen.fill((20, 100, 150))  # Fill the screen with a color (e.g., light blue for water)

    for fish in fishes:
        fish.draw(screen)  # Draw each fish
    
    # Update the display
    pygame.display.flip()

pygame.quit()