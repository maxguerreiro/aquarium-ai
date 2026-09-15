import pygame

pygame.init()

# Set up the display

WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Aquarium AI")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., light blue for water)
    screen.fill((20, 100, 150))

    # Update the display
    pygame.display.flip()

pygame.quit()