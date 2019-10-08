import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from ca_models_multiprocess import Grid
import random

SCREEN_SIZE = [1200, 900]
CELL_SIZE = 15
BACKGROUND_COLOR = [0, 0, 0]
DEAD_RATIO = 1 / 3

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
    chances = list([1 for dead in range(int(1 / DEAD_RATIO - 1))])
    chances.append(0)
    for cell_row in grid.cells:
        for cell in cell_row:
            cell.alive = random.choice(chances)

    running = True
    while running:
        events = pygame.event.get()
        clock.tick(30)
        running = listen_quit(events)

        grid.update()
        
        pygame.display.flip()

if __name__ == '__main__':
    main_loop()
