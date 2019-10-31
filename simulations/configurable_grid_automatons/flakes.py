import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from ca_models_2 import Grid, Capture
import random

SCREEN_SIZE = [1600, 900]
CELL_SIZE = 1
BACKGROUND_COLOR = [0, 0, 0]
DEAD_RATIO = 3 / 7

def listen_quit(events_list):
    for event in events_list:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
        elif event.type == QUIT:
            return False
    return True

def main_loop():
    pygame.init()

    clock = pygame.time.Clock()
    main_window = pygame.display.set_mode(SCREEN_SIZE)
    capture = Capture()

    grid = Grid(CELL_SIZE, 'flakes', aging=True)
    chances = list([1 for dead in range(int(1 / DEAD_RATIO - 1))])
    chances.append(0)
    seedline_cols = set([random.randrange(grid.num_columns) for column in range(random.randrange(10, 20))])
    for row_idx, cell_row in enumerate(grid.cells):
        if row_idx in seedline_cols:
            for cell in cell_row:
                cell.toggle_cell(random.choice(chances))

    grid.manual_update_states()

    running = True
    while running:
        events = pygame.event.get()
        clock.tick(19)
        running = listen_quit(events)

        grid.update()
        capture.screen_shot()
        pygame.display.flip()

if __name__ == '__main__':
    main_loop()
