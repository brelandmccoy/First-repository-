# Import required libraries
import pygame, sqlite3, random

# Initialize Pygame and set up game constants
pygame.init()
DIMS = {'SCREEN': (800, 600), 'PADDLE': (100, 15), 'BRICK': (60, 20), 'BALL': 10}
COLORS = {'WHITE': (255, 255, 255), 'BLUE': (0, 0, 255), 'RED': (255, 0, 0), 'GREEN': (0, 255, 0)}

class Breakout:
    def __init__(self):
        # Set up the game window and initial settings
        self.screen = pygame.display.set_mode(DIMS['SCREEN'])
        pygame.display.set_caption("Breakout Game")
        self.font = pygame.font.Font(None, 36)
        self.db_path = r"C:\Users\BIS11\Desktop\Notes\Notes for coding\highscores.db"
        # Create high scores database if it doesn't exist
        with sqlite3.connect(self.db_path) as conn:
            conn.cursor().execute('CREATE TABLE IF NOT EXISTS highscores (name TEXT, score INTEGER)')
        self.reset_game(1, True)
        
    def reset_game(self, level, full_reset=False):
        if full_reset:
            self.score, self.lives, self.level = 0, 3, level
        else:
            self.level = level
        # Position paddle and ball
        self.paddle = pygame.Rect(DIMS['SCREEN'][0]//2 - DIMS['PADDLE'][0]//2, DIMS['SCREEN'][1]-30, *DIMS['PADDLE'])
        self.ball = pygame.Rect(DIMS['SCREEN'][0]//2 - DIMS['BALL'], DIMS['SCREEN'][1]-50, DIMS['BALL']*2, DIMS['BALL']*2)
        self.ball_dx = self.ball_dy = 4 + (level - 1)
        self.ball_dy *= -1
        # Generate bricks
        self.bricks = [
            pygame.Rect(
                col*(DIMS['BRICK'][0]+5)+(DIMS['SCREEN'][0]-(min(10+level-1,13)*(DIMS['BRICK'][0]+5)))//2,
                row*(DIMS['BRICK'][1]+5)+80, *DIMS['BRICK']
            )
            for row in range(min(5+level-1,8))
            for col in range(min(10+level-1,13))
        ]
    
    def get_high_score(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                result = conn.cursor().execute(
                    "SELECT name, score FROM highscores ORDER BY score DESC LIMIT 1"
                ).fetchone()
                return result if result else (None, 0)
        except:
            return (None, 0)
        
    def save_high_score(self):
        if self.score > self.get_high_score()[1]:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM highscores")
                c.execute("INSERT INTO highscores VALUES (?, ?)", (self.player_name, self.score))
    
    def run(self):
        name_input = ""
        clock = pygame.time.Clock()
        while True:
            self.screen.fill(COLORS['WHITE'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name_input.strip():
                        self.player_name = name_input.strip()
                        return self.game_loop()
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    elif (len(name_input) < 15 and event.unicode.isalnum()) or event.unicode.isspace():
                        name_input += event.unicode
            self.screen.blit(
                self.font.render("Enter your name (press Enter when done):", True, COLORS['RED']),
                (DIMS['SCREEN'][0]//4, DIMS['SCREEN'][1]//2 - 50)
            )
            self.screen.blit(
                self.font.render(name_input + "|", True, COLORS['RED']),
                (DIMS['SCREEN'][0]//4, DIMS['SCREEN'][1]//2)
            )
            pygame.display.flip()
            clock.tick(60)
    
    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            self.screen.fill(COLORS['WHITE'])

            # Handle paddle movement
            keys = pygame.key.get_pressed()
            self.paddle.x = max(0, min(DIMS['SCREEN'][0] - DIMS['PADDLE'][0],
                                       self.paddle.x + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 8))

            # Move ball
            self.ball.x += self.ball_dx
            self.ball.y += self.ball_dy

            # Handle wall collisions
            if self.ball.left <= 0:
                self.ball.left = 0
                self.ball_dx = abs(self.ball_dx)
            elif self.ball.right >= DIMS['SCREEN'][0]:
                self.ball.right = DIMS['SCREEN'][0]
                self.ball_dx = -abs(self.ball_dx)
            if self.ball.top <= 0:
                self.ball.top = 0
                self.ball_dy = abs(self.ball_dy)

            # Paddle collision
            if self.ball.colliderect(self.paddle):
                self.ball.bottom = self.paddle.top
                self.ball_dx = max(min(-((self.paddle.centerx - self.ball.centerx) / (DIMS['PADDLE'][0] / 2)) * 5, 8), -8)
                self.ball_dy = -max(abs(self.ball_dy), 4)

            # Brick collisions
            for brick in self.bricks[:]:
                if self.ball.colliderect(brick):
                    self.bricks.remove(brick)
                    self.score += 10 * self.level
                    if self.ball.centerx >= brick.left and self.ball.centerx <= brick.right:
                        self.ball_dy *= -1
                    else:
                        self.ball_dx *= -1

            # Ball lost
            if self.ball.top >= DIMS['SCREEN'][1]:
                self.lives -= 1
                if self.lives <= 0:
                    self.save_high_score()
                    self.reset_game(1, True)
                else:
                    self.ball = pygame.Rect(DIMS['SCREEN'][0]//2 - DIMS['BALL'], DIMS['SCREEN'][1]-50, DIMS['BALL']*2, DIMS['BALL']*2)
                    self.ball_dx = random.choice([-4, 4])
                    self.ball_dy = -4

            # Level completed
            if not self.bricks:
                self.reset_game(self.level + 1)

            # Rendering
            for brick in self.bricks:
                pygame.draw.rect(self.screen, COLORS['GREEN'], brick)
            pygame.draw.rect(self.screen, COLORS['BLUE'], self.paddle)
            pygame.draw.circle(self.screen, COLORS['RED'], self.ball.center, DIMS['BALL'])

            # Score display
