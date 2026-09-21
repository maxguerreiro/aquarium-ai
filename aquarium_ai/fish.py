from pathlib import Path

import pygame


class Fish:
    _sprite = None
    _sprite_path = Path(__file__).resolve().parent / "assets" / "sprites" / "fish.png"
    _sprite_width = 40

    def __init__(self, x, y, speed, direction):
        self.position = pygame.Vector2(x, y)
        self.speed = speed
        self.direction = pygame.Vector2(direction)  # Initial direction
        self.radius = 20

    def move(self, action, dt, width, height):

        direction = pygame.Vector2(
            float(action[0]),
            float(action[1])
        )

        # Avoid normalizing a zero vector
        if direction.length_squared() > 0:

            direction = direction.normalize()

            self.direction = direction

        # Move using the fish's existing speed
        self.position += self.direction * self.speed * dt

        # Keep the fish inside the aquarium
        self.position.x = max(
            self.radius,
            min(width - self.radius, self.position.x)
        )

        self.position.y = max(
            self.radius,
            min(height - self.radius, self.position.y)
        )

    def get_observation(self, shark, width, height):

        return [
            self.position.x / width,
            self.position.y / height,

            (shark.position.x - self.position.x) / width,
            (shark.position.y - self.position.y) / height,

            self.direction.x,
            self.direction.y
        ]

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

    @classmethod
    def _load_sprite(cls):
        if cls._sprite is None:
            source = pygame.image.load(cls._sprite_path).convert_alpha()
            width = cls._sprite_width
            height = round(source.get_height() * width / source.get_width())
            cls._sprite = pygame.transform.smoothscale(source, (width, height))
        return cls._sprite

    def draw(self, screen):
        sprite = self._load_sprite()
        angle = -pygame.Vector2(1, 0).angle_to(self.direction)
        rotated_sprite = pygame.transform.rotate(sprite, angle)
        rect = rotated_sprite.get_rect(center=self.position)
        screen.blit(rotated_sprite, rect)
