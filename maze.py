import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Builder vs. Skapy")

# Clock
clock = pygame.time.Clock()
FPS = 10

# Simple maze: 1 = wall, 0 = path
maze = [[1 if random.random() < 0.2 else 0 for _ in range(COLS)] for _ in range(ROWS)]
for i in range(ROWS):
    maze[i][0] = 1
    maze[i][COLS-1] = 1
for j in range(COLS):
    maze[0][j] = 1
    maze[ROWS-1][j] = 1

# Player (Skapy) and Enemy
player_pos = [1, 1]  # [row, col]
enemy_pos = [ROWS - 2, COLS - 2]

# Exit
exit_pos = [ROWS - 2, 1]

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.draw.rect(screen, BLUE, (*[i * TILE_SIZE for i in reversed(player_pos)], TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, RED, (*[i * TILE_SIZE for i in reversed(enemy_pos)], TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, (0, 255, 0), (*[i * TILE_SIZE for i in reversed(exit_pos)], TILE_SIZE, TILE_SIZE))

def move_player(dy, dx):
    new_y = player_pos[0] + dy
    new_x = player_pos[1] + dx
    if 0 <= new_y < ROWS and 0 <= new_x < COLS and maze[new_y][new_x] == 0:
        player_pos[0] = new_y
        player_pos[1] = new_x

def move_enemy():
    # Simple patrol: random direction
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    random.shuffle(directions)
    for dy, dx in directions:
        new_y = enemy_pos[0] + dy
        new_x = enemy_pos[1] + dx
        if 0 <= new_y < ROWS and 0 <= new_x < COLS and maze[new_y][new_x] == 0:
            enemy_pos[0] = new_y
            enemy_pos[1] = new_x
            break

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    draw_maze()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move_player(-1, 0)
    elif keys[pygame.K_DOWN]:
        move_player(1, 0)
    elif keys[pygame.K_LEFT]:
        move_player(0, -1)
    elif keys[pygame.K_RIGHT]:
        move_player(0, 1)

    move_enemy()

    # Win/Lose Conditions
    if player_pos == exit_pos:
        print("Skapy wins! Escaped the maze.")
        running = False
    if player_pos == enemy_pos:
        print("Caught by agent! Maze Builder wins.")
        running = False

pygame.quit()

