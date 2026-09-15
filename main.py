import random
import pygame

from fish import Fish
from shark import Shark


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

shark = Shark(WIDTH / 2, HEIGHT / 2, 200)  # Create a shark instance at the center of the screen

running = True

score = 0  # Initialize score

while running:

    dt = clock.tick(60) / 1000  # Amount of seconds between each loop (Delta time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update fish position
    for fish in fishes:
        fish.update(dt, WIDTH, HEIGHT)

    # Update shark position
    shark.update(dt, WIDTH, HEIGHT)

    for fish in fishes[:]:  # Iterate over a copy of the list

        if shark.collide_with(fish):
            fishes.remove(fish)  # Remove the fish if the shark collides with it

            score += 1  # Increment score for each fish eaten


    screen.fill((20, 100, 150))  # Fill the screen with a color (e.g., light blue for water)

    for fish in fishes:
        fish.draw(screen)  # Draw each fish

    shark.draw(screen)  # Draw the shark

    font = pygame.font.Font(None, 36)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

pygame.quit()