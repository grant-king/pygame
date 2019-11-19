import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from ca_models_2 import Grid, Capture, Control
import random
import os
import cv2

SCREEN_SIZE = [1600, 900]
CELL_SIZE = 4
BACKGROUND_COLOR = [0, 0, 0]

def main_loop():
    pygame.init()

    clock = pygame.time.Clock()
    main_window = pygame.display.set_mode(SCREEN_SIZE)
    
    grid = Grid(CELL_SIZE, 'walledcities', aging=1)
    capture = Capture(grid)
    control = Control(capture)
    
    #grid.random_seed()
    capture.load_image("D:/chaos/extra/cat_people.jpg")
    control.step_clock.set_timer(QUIT, 50) #auto off after n steps
    control.step_clock.set_timer(control.STATESHOTEVENT, 1) #capture state every n steps
    
    for _ in range(9):
        control.running
        grid.update()
        capture.screen_shot()
        pygame.display.set_caption(f'{grid.rule_set.name} step {grid.rule_set.run_ticks}')
        pygame.display.flip()
        capture.save_image()

    grid.set_rules('coral')

    while control.running:
        #change ruleset
        grid.update()
        capture.screen_shot()
        pygame.display.set_caption(f'{grid.rule_set.name} step {grid.rule_set.run_ticks}')
        pygame.display.flip()
        capture.save_image()

    #capture last state before quit        
    capture.state_shot()
    pygame.quit()

if __name__ == '__main__':
    main_loop()
