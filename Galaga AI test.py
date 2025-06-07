import pygame
import random
import math

#initialize pygame
pygame.init()

# screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga AI")
clock = pygame.time.Clock()

# Game settings
PLAYER_SPEED = 10
BULLET_SPEED = 30
BASE_ENEMY_SPEED = 2
ENEMY_WAVE_AMPLITUDE = 50
ENEMY_WAVE_FREQUENCY = 0.03
INITIAL_LIVES = 30
SHOOT_COOLDOWN = 8 # Frames between shots

# Game state
player_mode = "AI" #options: "AI" or "Human"
paused = False
score = 0 
level = 1
enemies_destroyed = 0
game_over = False

# Player class
class Player:
    def __init__(self):
        self.image = pygame.surface((40, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.direction = 1 # Moving right
        self.bullets = []
        self.lives = INITIAL_LIVES
        self.shoot_timer = 0
        
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.lives = INITIAL_LIVES
        self.bullets.clear()
        self.shoot_timer = 0
    
    def move_ai(self, enemies):
        closest_enemy = min(enemies, key=lambda e: abs(e.rect.x - self.rect.x))
        
        # Avoid collision or align with enemy
        if closest_enemy.rect.y> 80 and abs(closest_enemy.rect.x - self.rect.x) < 90:
            if closest_enemy.rect.x  < self.rect.x:
                self.direction = 1 # Move right
            else:
                self.direction = -1 # Move left
        else:
            self.direction = 1 if closest_enemy.rect.x > self.rect.x else -1
            
        # Apply movement
        self.rect.x += PLAYER_SPEED * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
    
    def move_human(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
            
    def shoot(self):
        if self.shoot_timer == 0:
            bullet = bullet(self.rect.centerx, self.rect.top)
            self.bullets.append(bullet)
            self.shoot_timer = SHOOT_COOLDOWN
            
    def update(self, enemies):
        if player_mode == "AI":
            self.move_ai(enemies)
            self.shoot()
        else:
            keys = pygame.key.get_pressed()
            self.move_human(keys)
            if keys[pygame.K_SPACE]:
                self.shoot()
                
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
            
        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
                
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
            
    def lose_life(self):
        self.lives -= 1
        
# enemy class
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.surface((40,40))
        self.image.fill(RED)
        self
        self.origin_x = x
        self.time = 0
        
    def move(self):
        self.rect.y += BASE_ENEMY_SPEED + (level * 0.5) # Increase speed with level
        self.rect.x = self.origin_x + math.sin(self.time * ENEMY_WAVE_AMPLITUDE) * ENEMY_WAVE_AMPLITUDE
        self.time += 1
            
        # Speed wrap logic
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -40 # Wrap to the top of the screen
                
    def draw(self):
        self.move()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.rect.y -= BULLET_SPEED
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# initialize game objects
player = Player()
enemies = [Enemy(random.randint(100,700), random.randit(-300, -50)) for _ in range(5)]

def reset_game():
    global score, level, enemies_destroyed, game_over
    player.reset()
    enemies.clear()
    for _ in range(5):
        enemies.append(Enemy(random.randint(100, 700), random.randint(-300, -50)))
    score = 0
    level = 1
    enemies_destroyed = 0
    game_over = False
    
def draw_pause_menu():
    screen.fill(BLACK)
    font = pygame.font.Sysfont(None, 48)
    menu_text = font.render("PAUSE MENU", True, WHITE)
    mode_text = font.render("Press M to toggle AI/Human mode", True, WHITE)
    resume_text = font.render("Press ESC to resume", True, WHITE)
    
    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 200))
    screen.blit(mode_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 260))
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 320))
    
def draw_game_over():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("GAME OVER", True, RED)
    restart_text = font.render("Press R to Restart", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 320))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif paused and event.key == pygame.K_m:
                player_mode = "Human" if player_mode == "AI" else "AI"
            elif game_over and event.key == pygame.K_r:
                reset_game()
    
    if not paused and not game_over:
        # Update game objects
        player.update(enemies)
        for enemy in enemies:
            enemy.update()
        
        # Collision detection (bullets vs enemies)
        for bullet in player.bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    player.bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(Enemy(random.randint(100, 700), random.randint(-300, -50)))
                    score += 100
                    enemies_destroyed += 1
                    break
        
        # Collision detection (player vs enemies)
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player.lose_life()
                enemy.rect.y = random.randint(-200, -50)
                enemy.origin_x = random.randint(50, SCREEN_WIDTH - 50)
                if player.lives <= 0:
                    game_over = True
        
        
        if enemies_destroyed >= 10:
            level += 1
            enemies_destroyed = 0 
        
        # Draw everything
        screen.fill(BLACK)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
            
        # Display score, lives, and level
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(level_text, (10, 70))
    
    elif game_over:
        draw_game_over()
        
    else:
        draw_pause_menu()
    
    # Update the display
    pygame.display.flip()
    
    # cap the frame rate
    clock.tick(60)
    
# Quit pygame
pygame.quit()