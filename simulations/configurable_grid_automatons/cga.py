import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from ca_models_2 import Grid, Capture, Control
import random
import os
import cv2

SCREEN_SIZE = [1600, 900]
CELL_SIZE = 5
BACKGROUND_COLOR = [0, 0, 0]
DEAD_RATIO = 2 / 7


def main_loop():
    pygame.init()

    clock = pygame.time.Clock()
    main_window = pygame.display.set_mode(SCREEN_SIZE)
    
    grid = Grid(CELL_SIZE, 'replicator', aging=1)
    capture = Capture(grid)
    control = Control(capture)
    
    chances = list([1 for dead in range(int(1 / DEAD_RATIO - 1))])
    chances.append(0)
    seedline_cols = set([random.randrange(grid.num_columns) for column in range(random.randrange(10, grid.num_columns/5))])
    for row_idx, cell_row in enumerate(grid.cells):
        if row_idx in seedline_cols:
            for cell in cell_row:
                cell.toggle_cell(random.choice(chances))
     
    grid.manual_update_states()

    while control.running:
        clock.tick(19)
        
        grid.update()
        capture.screen_shot()
        pygame.display.set_caption(f'{grid.rule_set.name} step {grid.rule_set.run_ticks}')
        pygame.display.flip()
    #capture last state before quit        
    capture.state_shot()
    capture.save_image()
    pygame.quit()

if __name__ == '__main__':
    main_loop()
