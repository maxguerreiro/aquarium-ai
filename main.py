import pygame

from aquarium import Aquarium


pygame.init()

WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Aquarium AI")

clock = pygame.time.Clock()

aquarium = Aquarium(WIDTH, HEIGHT, 10)

font = pygame.font.Font(None, 36)

running = True

while running:

    dt = clock.tick(60) / 1000

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Update simulation
    aquarium.update(dt)

    # Render
    screen.fill((20, 100, 150))

    aquarium.draw(screen)

    # Score
    score_text = font.render(
        f"Peixes comidos: {aquarium.score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (20, 20))

    pygame.display.flip()


pygame.quit()