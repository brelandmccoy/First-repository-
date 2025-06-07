import pygame
import random

# Initialize
pygame.init()

# Screen/grid setup
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE *ROWS
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
CLOCK = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Tetromino shapes with full rotation states
SHAPES  =  [
    [   #  I
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]    
    ],
    [   # J
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0]
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    [   # L
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ],
    [  # O (no rotation needed)
        [[1, 1],
        [1, 1]]
    ],
    [   # S
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    [   # T
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]],
    ],
    [   # Z
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]],
    ]
]

# Grid builder
def create_grid(locked={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLUMNS):
            if (x, y) in locked:
                grid[y][x] =  locked[(x, y)]
    return grid

# piece class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS
        self.rotation = 0
    
    def image(self):
        return self.shape[self.rotation % len(self.shape)]
    
    def cells(self):
        positions = []
        shape = self.image()
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val == 1:
                    positions.append((self.x + j, self.y + i))
        return positions

# Helper functions
def convert_shape_format(piece):
    return piece.cells()

def valid_space(piece, grid):
    valid = [[(j, i) for j in range(COLUMNS) if grid [i][j] == BLACK] for i in range(ROWS)]
    valid = [pos for row in valid for pos in row]
    for pos in convert_shape_format(piece):
        if pos not in valid:
            if pos[1] >= 0:
                return False
    return True

def check_lost(locked):
    return any( y < 1 for (_, y) in locked)

def get_shape():
    return Piece(3, 0, random.choice(SHAPES))

def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(SCREEN, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for y in range(ROWS):
        pygame.draw.line(SCREEN, GRAY, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))
    for x in range(COLUMNS):
        pygame.draw.line(SCREEN, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))

def clear_rows(grid, locked):
    cleared = 0
    for y in range(ROWS - 1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            for x in range(COLUMNS):
                try:
                    del locked[(x, y)]
                except:
                    continue
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, y_ = key
                if y_ < y:
                    locked[(x, y_ + 1)] = locked.pop ((x, y_))
    return cleared

def draw_window(grid):
    SCREEN.fill(BLACK)
    draw_grid(grid)
    pygame.display.update()
    
# Main game loop
def main():
    locked_positions = {}
    current_piece = get_shape()
    next_piece = get_shape()
    grid = create_grid(locked_positions)
        
    fall_time = 0
    fall_speed = 0.4
    running = True
    
    while running:
        grid = create_grid(locked_positions)
        fall_time += CLOCK.get_rawtime()
        CLOCK.tick()
        
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y += 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                current_piece = get_shape()
                next_piece = get_shape()
                if check_lost(locked_positions):
                    running = False
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece):
                        current_piece.rotation -= 1
                        
        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                grid[y][x] = current_piece.color
                
        clear_rows(grid, locked_positions)
        draw_grid(grid)
    pygame.quit()
# Start game
if __name__ == "_main_":
    main()