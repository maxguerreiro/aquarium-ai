import pygame

class Fish:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 20

    def update(self, dt, screen_width):
        self.x += self.speed * dt
        # Keep the fish within the screen bounds
        if self.x - self.radius > screen_width:
            self.x = -self.radius
            

    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            (255, 100, 50), 
            (int(self.x), int(self.y)), self.radius)  # Draw the fish as a circle