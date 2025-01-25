# Повний код гри
import pygame
import random

# ініціалізація Pygame
pygame.init()
pygame.font.init()

# Налаштування екрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Clone")

# Кольори
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Клас для гравця
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - 70, 50, 50)
        self.color = BLUE
        self.gravity = 0.5
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_count = 0

    def jump(self):
        if self.jump_count < 2:
            self.velocity_y = -10
            self.is_jumping = True
            self.jump_count += 1

    def move(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= HEIGHT - 70:
            self.rect.y = HEIGHT - 70
            self.is_jumping = False
            self.jump_count = 0
            self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Клас для перешкод
class Obstacle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def move(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

# Головна гра
def main():
    clock = pygame.time.Clock()
    player = Player()
    obstacles = []
    obstacles_range = 5
    for i in range(obstacles_range):
        width = 50
        height = random.randint(50, 100)
        x = random.randint(800, 1200)
        y = HEIGHT - 70
        obstacle = Obstacle(x,y,width,height,RED)
        obstacles.append(obstacle)
    speed = 5
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Рух гравця та перешкоди
        player.move()
        for obstacle in obstacles:
            obstacle.move(speed)
            if obstacle.rect.x < 0:
                obstacle.reset_position(random.randint(800, 1200), HEIGHT - 70)

            if player.rect.colliderect(obstacle.rect):
                lose = pygame.font.SysFont("Arial", 78).render("You lose", True, (255, 0, 0))
                screen.blit(lose, (300, 250))
                pygame.display.flip()
                pygame.time.delay(1000)
                running = False

        # Малювання
        screen.fill(WHITE)
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Запуск гри
if __name__ == "__main__":
    main()