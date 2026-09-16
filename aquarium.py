import random
import pygame

from fish import Fish
from shark import Shark


class Aquarium:

    def __init__(self, width, height, fish_count=10):

        self.width = width
        self.height = height

        self.fish_count = fish_count

        self.max_steps = 300

        self.reset()

    def create_random_fish(self):

        radius = 20

        for _ in range(100):

            x = random.randint(
                radius,
                self.width - radius
            )

            y = random.randint(
                radius,
                self.height - radius
            )

            position = pygame.Vector2(x, y)

            distance = position.distance_to(
                self.shark.position
            )

            if distance > self.shark.radius + radius + 50:
                break

        else:
            raise RuntimeError(
                "Não foi possível encontrar uma posição válida para o peixe."
            )

        speed = random.randint(50, 150)

        direction = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        else:
            direction = direction.normalize()

        return Fish(x, y, speed, direction)

    def update(self, dt, action=None):

        self.current_step += 1

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

    def get_observation(self):

        shark = self.shark

        target = self.shark.find_closest_fish(self.fishes)

        #No target fish
        if target is None:
            return [
                shark.position.x / self.width,
                shark.position.y / self.height,
                0,
                0,
                shark.direction.x,
                shark.direction.y
            ]

        #Relative position
        relative_position = target.position - shark.position

        return [
            shark.position.x / self.width,
            shark.position.y / self.height,

            relative_position.x / self.width,
            relative_position.y / self.height,
            
            shark.direction.x,
            shark.direction.y
        ]

    def reset(self):

        self.score = 0

        self.current_step = 0

        self.shark = Shark(
            self.width / 2,
            self.height / 2,
            250
        )

        self.fishes = []

        for _ in range(self.fish_count):
            self.fishes.append(self.create_random_fish())

        return self.get_observation()

    def is_done(self):
        return self.current_step >= self.max_steps