import pygame

class Fish:
    def __init__(self, x, y, speed, direction):
        self.position = pygame.Vector2(x, y)
        self.speed = speed
        self.direction = pygame.Vector2(direction)  # Initial direction
        self.radius = 20

    def update(self, dt, screen_width, screen_height):

        self.position += self.direction * self.speed * dt

        # Update the position based on the direction and speed
        if self.position.x - self.radius > screen_width:
            self.position.x = -self.radius

        elif self.position.x + self.radius < 0:
            self.position.x = screen_width + self.radius

        if self.position.y - self.radius > screen_height:
            self.position.y = -self.radius

        elif self.position.y + self.radius < 0:
            self.position.y = screen_height + self.radius
            

    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            (255, 100, 50), 
            (int(self.position.x), int(self.position.y)), self.radius)  # Draw the fish as a circle