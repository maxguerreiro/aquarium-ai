from fish import Fish
import pygame

pygame.init()

# Set up the display

WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aquarium AI")

clock = pygame.time.Clock()

# Fish
fish = Fish(100, 350, 200)  # Starting position (100, 350) and speed of 200 pixels per second
fish2 = Fish(500, 200, 100)  # Another fish with different starting position and speed

running = True

while running:

    dt = clock.tick(60) / 1000  # Amount of seconds between each loop (Delta time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update fish position
    fish.update(dt, WIDTH)
    fish2.update(dt, WIDTH)

    screen.fill((20, 100, 150))  # Fill the screen with a color (e.g., light blue for water)

    fish.draw(screen)
    fish2.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()