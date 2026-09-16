import pygame

class Fish:
    def __init__(self, x, y, speed, direction):
        self.position = pygame.Vector2(x, y)
        self.speed = speed
        self.direction = pygame.Vector2(direction)  # Initial direction
        self.radius = 20

    def update(self, dt, screen_width, screen_height):

    # Update position
        self.position += self.direction * self.speed * dt

        # Horizontal collision
        if self.position.x - self.radius < 0:

            self.position.x = self.radius

            self.direction.x *= -1

        elif self.position.x + self.radius > screen_width:

            self.position.x = screen_width - self.radius

            self.direction.x *= -1

        # Vertical collision
        if self.position.y - self.radius < 0:

            self.position.y = self.radius

            self.direction.y *= -1

        elif self.position.y + self.radius > screen_height:

            self.position.y = screen_height - self.radius

            self.direction.y *= -1
            

    def draw(self, screen):

        # Direção perpendicular à direção do movimento
        perpendicular = pygame.Vector2(
            -self.direction.y,
            self.direction.x
        )

        # Ponta da cabeça
        front = self.position + self.direction * self.radius

        # Parte superior e inferior do corpo
        top = self.position + perpendicular * self.radius * 0.6
        bottom = self.position - perpendicular * self.radius * 0.6

        # Parte traseira
        back = self.position - self.direction * self.radius

        # Corpo
        pygame.draw.polygon(
            screen,
            (255, 100, 50),
            [
                front,
                top,
                back,
                bottom
            ]
        )

        # Cauda
        tail_center = self.position - self.direction * self.radius

        tail_top = (
            tail_center
            + perpendicular * self.radius * 0.7
            - self.direction * self.radius * 0.8
        )

        tail_bottom = (
            tail_center
            - perpendicular * self.radius * 0.7
            - self.direction * self.radius * 0.8
        )

        pygame.draw.polygon(
            screen,
            (255, 180, 50),
            [
                tail_center,
                tail_top,
                tail_bottom
            ]
    )