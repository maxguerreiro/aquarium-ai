from pathlib import Path

import pygame


class Shark:
    _sprite = None
    _sprite_path = Path(__file__).resolve().parent / "assets" / "sprites" / "shark.png"
    _sprite_width = 70

    def __init__(self, x, y, speed):
        self.position = pygame.Vector2(x, y)
        self.speed = speed
        self.direction = pygame.Vector2(1, 0)  # Initial direction
        self.radius = 35

    def update(self, dt, screen_width, screen_height):

        keys = pygame.key.get_pressed()

        movement = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1

        if movement.length() > 0:
            movement = movement.normalize()
            self.direction = movement  # Update direction based on movement
            self.position += movement * self.speed * dt

        # Keep the shark within the screen bounds
        self.position.y = max(
            self.radius,
            min(screen_height - self.radius, self.position.y)
        )

        self.position.x = max(
            self.radius,
            min(screen_width - self.radius, self.position.x)
        )

    def draw(self, screen):
        sprite = self._load_sprite()
        angle = -pygame.Vector2(1, 0).angle_to(self.direction)
        rotated_sprite = pygame.transform.rotate(sprite, angle)
        rect = rotated_sprite.get_rect(center=self.position)
        screen.blit(rotated_sprite, rect)

    @classmethod
    def _load_sprite(cls):
        if cls._sprite is None:
            source = pygame.image.load(cls._sprite_path).convert_alpha()
            width = cls._sprite_width
            height = round(source.get_height() * width / source.get_width())
            cls._sprite = pygame.transform.smoothscale(source, (width, height))
        return cls._sprite

    def collide_with(self, fish):
        distance = self.position.distance_to(fish.position)
        return distance <= (self.radius + fish.radius)

    def find_closest_fish(self, fishes):
        closest_fish = None
        min_distance = float('inf')

        for fish in fishes:
            distance = self.position.distance_to(fish.position)
            if distance < min_distance:
                min_distance = distance
                closest_fish = fish

        return closest_fish

    def hunt(self, fishers):

        target = self.find_closest_fish(fishers)

        if target is None:
            return pygame.Vector2(0, 0)  # No fish to hunt

        direction = target.position - self.position

        if direction.length() > 0:
            return direction.normalize()

        return pygame.Vector2(0, 0)

    def move(self, action, dt, screen_width, screen_height):

        movement = pygame.Vector2(action)

        if movement.length() > 0:

            movement = movement.normalize()

            self.direction = movement

            self.position += movement * self.speed * dt

        # Aquarium boundaries
        self.position.x = max(
            self.radius,
            min(screen_width - self.radius, self.position.x)
        )

        self.position.y = max(
            self.radius,
            min(screen_height - self.radius, self.position.y)
        )
