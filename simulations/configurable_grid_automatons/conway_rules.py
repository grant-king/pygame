import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from ca_models import Grid
import random

SCREEN_SIZE = [1920, 1080]
CELL_SIZE = 60
BACKGROUND_COLOR = [0, 0, 0]

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

    grid = Grid(CELL_SIZE, 'conway')
    for cell_row in grid.cells[:10:2]:
        random.choice(cell_row).alive = True

    running = True
    while running:
        events = pygame.event.get()
        clock.tick(10)
        running = listen_quit(events)

        grid.update()
        
        pygame.display.flip()

if __name__ == '__main__':
    main_loop()
    