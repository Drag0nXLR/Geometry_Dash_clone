import sys

import pygame
import random

# Ініціалізація Pygame
pygame.init()
pygame.mixer.init()

# Налаштування екрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale(pygame.image.load("dggqyse-76b77fd2-a577-44f7-b3f4-151cdec2a610.png"), (WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Clone")
jump_sound = pygame.mixer.Sound("jump-15984.mp3")
muzon = pygame.mixer.music.load("aboard-a-aurora-game-menu-pulse-203549.mp3")
pygame.mixer.music.play(-1)

# Колір
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Клас для гравця
class Player:
    def __init__(self):
        self.image = pygame.image.load('kubik.png')  # Завантаження зображення
        self.image = pygame.transform.scale(self.image, (30, 30))  # Зменшення розміру зображення
        self.rect = self.image.get_rect(center=(100, HEIGHT - 60))
        self.jump_count = 0
        self.jump_height = 10
        self.gravity = 0.5
        self.vel_y = 0

    def jump(self):
        if self.jump_count < 3:  # Три стрибки
            self.vel_y = -self.jump_height
            self.jump_count += 1
            jump_sound.play()

    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Скидання стрибків при досягненні землі
        if self.rect.y >= HEIGHT - 30:
            self.rect.y = HEIGHT - 30
            self.vel_y = 0
            self.jump_count = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Клас для перешкод
class Obstacle:
    def __init__(self, w, h):
        self.image = pygame.image.load("spike_by_greaterhtrae_dgqdoe4-fullview.png")
        self.image = pygame.transform.scale(self.image, (w, h))  # Колір перешкоди
        self.rect = self.image.get_rect(center=(WIDTH + 50, HEIGHT - 30))

    def move(self):
        self.rect.x -= 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Основний цикл гри
def main():
    clock = pygame.time.Clock()
    player = Player()
    obstacles = [Obstacle(random.randint(50, 100), 50)]
    game_over = False
    score = 0

    while True:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()

        if not game_over:
            # Додати нові перешкоди
            if random.randint(1, 100) < 5:
                obstacles.append(Obstacle(random.randint(50, 100), 50))

            # Переміщення гравця та перешкод
            player.move()
            for obstacle in obstacles:
                obstacle.move()

                # Перевірка колізії
                if player.rect.colliderect(obstacle.rect):
                    game_over = True

                if obstacle.rect.x < 0:
                    obstacles.remove(obstacle)
                    score += 1

            # Малюємо гравця та перешкоди
            player.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            if score >= 200:
                font = pygame.font.Font(None, 74)
                text = font.render("You won!", True, (0, 0, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                sys.exit()
        else:
            # Виведення повідомлення про гру
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
