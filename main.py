import pygame as pg
import random

pg.init()

# Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAYING_WIDTH = 300
PLAYING_HEIGHT = 600
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAYING_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAYING_HEIGHT

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (153, 51, 255)
PINK = (255, 0, 255)
ORANGE = (255, 128, 0)

# SHAPES FORMAT
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '.00..',
      '.0...',
      '.0...',
      '.....'],
     ['.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '...0.',
      '...0.',
      '..00.',
      '.....']]

L = [['.....',
      '.0...',
      '.0...',
      '.00..',
      '.....'],
     ['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '...0.',
      '...0.',
      '.....'],
     ['.....',
      '.000.',
      '.0...',
      '.....',
      '.....']]

T = [['.....',
      '.000.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Index 0-6 Represent Shape and Color
shapes = [S, Z, I, O, J, L, T]
shapes_colors = [WHITE, PINK, BLUE, GREEN, RED, PURPLE, ORANGE]


# Shape Class
class Piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapes_colors[shapes.index(shape)]
        self.rotate = 0


# Create Lists in Lists Like [[(0,0,0)],[(0,0,0)],....]
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    # Grid is 20 Rows X 10 Column
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                grid[i][j] = locked_pos[(j, i)]
    return grid


# Draw The Grid Lines For Block Size
def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    for i in range(len(grid)):
        pg.draw.line(surface, (128, 128, 128), (sx, sy + (i * BLOCK_SIZE)), (sx + PLAYING_WIDTH, sy + (i * BLOCK_SIZE)))
        for j in range(len(grid[i])):
            pg.draw.line(surface, (128, 128, 128), (sx + (j * BLOCK_SIZE), sy),
                         (sx + (j * BLOCK_SIZE), sy + PLAYING_HEIGHT))


# Draw Text on Screen After Game Over
def draw_text_in_middle(surface, text, size, color):
    font = pg.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (int(TOP_LEFT_X + PLAYING_WIDTH / 2 - (label.get_width() / 2)),
                         int(TOP_LEFT_Y + PLAYING_HEIGHT / 2 - (label.get_height() / 2))))


# Draw A Red Rect Surround The Grid
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((255, 255, 255))

    # Game Name Above of The Grid
    pg.font.init()
    font = pg.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, BLACK)
    surface.blit(label, (int(TOP_LEFT_X + (PLAYING_WIDTH / 2) - (label.get_width()) / 2), 30))

    # Current Score
    font = pg.font.SysFont('comicsans', 30)
    score = font.render('Score: ' + str(score), 1, BLACK)
    sx = int(TOP_LEFT_X + PLAYING_WIDTH + 50)
    sy = int(TOP_LEFT_Y + PLAYING_HEIGHT / 2 - 100)
    surface.blit(score, (sx + 20, sy + 160))

    # Last Score
    label_last_score = font.render('High Score: ' + last_score, 1, BLACK)
    sx = int(TOP_LEFT_X - 200)
    sy = int(TOP_LEFT_Y + 200)
    surface.blit(label_last_score, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pg.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE,
                                               BLOCK_SIZE), 0)
    pg.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAYING_WIDTH, PLAYING_HEIGHT), 4)

    draw_grid(surface, grid)


# Update The File: score.txt
def update_score(new_score):
    score = max_score()

    with open("score.txt", 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))


# Getting The Max Score From The File: score.txt
def max_score():
    with open("score.txt", 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def get_shape():
    return Piece(5, 0, random.choice(shapes))


# Convert The Format of The Shape (List of 0 and . ) To Positions
# and Return The Current Position of The Blocks on Grid as a List
def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotate % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# Check When Piece Move if The Position on The Grid are Blocked With Color
def vaild_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def draw_next_shape(piece, surface):
    font = pg.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, BLACK)

    sx = int(TOP_LEFT_X + PLAYING_WIDTH + 50)
    sy = int(TOP_LEFT_Y + PLAYING_HEIGHT / 2 - 100)
    format = piece.shape[piece.rotate % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pg.draw.rect(surface, piece.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                             0)
    surface.blit(label, (sx + 10, sy - 20))


def clear_raws(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# Main Game
def main(surface):
    last_score = max_score()
    locked_pos = {}
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pg.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not vaild_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1
                    if not (vaild_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pg.K_RIGHT:
                    current_piece.x += 1
                    if not (vaild_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pg.K_DOWN:
                    current_piece.y += 1
                    if not (vaild_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pg.K_UP:
                    current_piece.rotate += 1
                    if not (vaild_space(current_piece, grid)):
                        current_piece.rotate -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_raws(grid, locked_pos) * 10

        draw_window(surface, grid, score, last_score)
        draw_next_shape(next_piece, surface)
        pg.display.update()

        if check_lost(locked_pos):
            draw_text_in_middle(surface, "YOY LOST!", 80, ORANGE)
            pg.display.update()
            pg.time.delay(1500)
            run = False
            update_score(score)


def main_menu():
    run = True
    while run:
        win.fill(WHITE)
        draw_text_in_middle(win, "Press Any Key To Play", 60, ORANGE)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                main(win)
    pg.display.quit()

    main(win)


win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Tetris")
main_menu()
