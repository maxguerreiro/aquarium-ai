import pygame

class Shark:

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

            perpendicular = pygame.Vector2(
                -self.direction.y,
                self.direction.x
            )

            front = (
                self.position
                + self.direction * self.radius
            )

            top = (
                self.position
                + perpendicular * self.radius * 0.6
            )

            bottom = (
                self.position
                - perpendicular * self.radius * 0.6
            )

            back = (
                self.position
                - self.direction * self.radius
            )

            pygame.draw.polygon(
                screen,
                (100, 120, 140),
                [
                    front,
                    top,
                    back,
                    bottom
                ]
    )

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