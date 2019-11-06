import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from ca_models_2 import Grid, Capture
import random
import os
import cv2

SCREEN_SIZE = [1600, 900]
CELL_SIZE = 10
BACKGROUND_COLOR = [0, 0, 0]
DEAD_RATIO = 2 / 7

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
    
    grid = Grid(CELL_SIZE, 'coral', aging=0)
    capture = Capture(grid)

    map_file_name = 'step_59.png' #input("type the file name to load: ")
    capture.load_state_shot(f'D:/chaos/coral_45/{map_file_name}')

    """
    chances = list([1 for dead in range(int(1 / DEAD_RATIO - 1))])
    chances.append(0)
    seedline_cols = set([random.randrange(grid.num_columns) for column in range(random.randrange(10, grid.num_columns/5))])
    for row_idx, cell_row in enumerate(grid.cells):
        if row_idx in seedline_cols:
            for cell in cell_row:
                cell.toggle_cell(random.choice(chances))
    """

    grid.manual_update_states()

    running = True
    while running:
        events = pygame.event.get()
        clock.tick(19)
        running = listen_quit(events)

        grid.update()
        capture.screen_shot()
        pygame.display.flip()
    #capture last state before quit        
    capture.state_shot()
    pygame.quit()

if __name__ == '__main__':
    main_loop()
