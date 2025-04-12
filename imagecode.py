import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blaster Xtreme")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 255, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("comicsans", 30)

# Placeholder Surfaces (can replace with images)
player_img = pygame.Surface((50, 40))
player_img.fill(GREEN)

bullet_img = pygame.Surface((5, 10))
bullet_img.fill((255, 255, 0))

enemy_img = pygame.Surface((40, 30))
enemy_img.fill(RED)

enemy_bullet_img = pygame.Surface((5, 10))
enemy_bullet_img.fill((255, 100, 100))

powerup_img = pygame.Surface((20, 20))
powerup_img.fill((0, 200, 255))

# Global Variables
player_speed = 5
bullet_speed = 7
enemy_speed = 2
enemy_bullet_speed = 4
score = 0
level = 1
game_over = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 60))
        self.speed = player_speed
        self.health = 3

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), random.randint(-100, -40)))
        self.speed = enemy_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(20, WIDTH - 20)
        if random.random() < 0.01:
            enemy_bullets.add(EnemyBullet(self.rect.centerx, self.rect.bottom))


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += enemy_bullet_speed
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), random.randint(-300, -40)))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Groups
player = Player()
player_group = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

for _ in range(5):
    enemies.add(Enemy())

# Game Loop
while True:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.add(Bullet(player.rect.centerx, player.rect.top))

    if not game_over:
        player_group.update(keys)
        bullets.update()
        enemies.update()
        enemy_bullets.update()
        powerups.update()

        # Collisions
        for hit in pygame.sprite.groupcollide(enemies, bullets, True, True):
            score += 1
            enemies.add(Enemy())
            if score % 10 == 0:
                level += 1
                for e in enemies:
                    e.speed += 0.3
                if random.random() < 0.5:
                    powerups.add(PowerUp())

        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.health -= 1

        if pygame.sprite.spritecollide(player, enemies, True):
            player.health -= 1
            enemies.add(Enemy())

        if pygame.sprite.spritecollide(player, powerups, True):
            player.health = min(5, player.health + 1)

        if player.health <= 0:
            game_over = True

    # Draw
    WIN.fill(BLACK)
    player_group.draw(WIN)
    bullets.draw(WIN)
    enemies.draw(WIN)
    enemy_bullets.draw(WIN)
    powerups.draw(WIN)

    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    WIN.blit(score_text, (10, 10))
    WIN.blit(health_text, (10, 40))
    WIN.blit(level_text, (10, 70))

    if game_over:
        game_over_text = font.render("GAME OVER - Press ESC to Quit", True, RED)
        WIN.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.update()
