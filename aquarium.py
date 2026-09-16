import random
import pygame

from fish import Fish
from shark import Shark


class Aquarium:

    def __init__(self, width, height, fish_count=10):

        self.width = width
        self.height = height

        self.fish_count = fish_count

        self.score = 0

        self.shark = Shark(
            width / 2,
            height / 2,
            250
        )

        self.fishes = []

        for _ in range(self.fish_count):
            self.fishes.append(self.create_random_fish())

    def create_random_fish(self):

        x = random.randint(50, self.width - 50)
        y = random.randint(50, self.height - 50)

        speed = random.randint(50, 150)

        direction = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

        if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
        else:
            direction = direction.normalize()

        return Fish(x, y, speed, direction)

    def update(self, dt, action=None):

        # Update fishes
        for fish in self.fishes:
            fish.update(dt, self.width, self.height)

        # Choose action
        if action is None:
            action = self.shark.hunt(self.fishes)

        # Move shark
        self.shark.move(
            action,
            dt,
            self.width,
            self.height
            )

        # Check collisions
        for fish in self.fishes[:]:

            if self.shark.collide_with(fish):

                self.fishes.remove(fish)

                self.score += 1

                self.fishes.append(self.create_random_fish())

    def draw(self, screen):

        for fish in self.fishes:
            fish.draw(screen)

        self.shark.draw(screen)