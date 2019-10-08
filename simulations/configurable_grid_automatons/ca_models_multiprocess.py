import pygame
import random
import os
import logging
import numpy as np
import numba
from numba import jit
from time import time, ctime

logging.basicConfig(
    filename = 'simulation.log', 
    level = logging.DEBUG, 
    format = '%(levelname)s: %(message)s', 
    filemode='a'
    )

class Grid:
    def __init__(self, cell_size, rule_name):
        self.SCREEN_SIZE = pygame.display.get_surface().get_size()
        self.CELL_SIZE = cell_size

        self.cells = []
        self.total_cells = 0
        self.cells_history = [] #list of sum of bools state history
        self.num_columns = self.SCREEN_SIZE[0] // self.CELL_SIZE
        self.num_rows = self.SCREEN_SIZE[1] // self.CELL_SIZE
        self.current_states = [[]]
        self.rule_set = Ruleset(rule_name)
        self.build_cells()

        logging.info(f'Grid initialized with {self.rule_set.name} rule at {ctime()} with {self.total_cells} cells')
          
    def check_static(self):
        if len(self.cells_history) > 24:
            first = self.cells_history[-24]
            same = 0
            for item in self.cells_history[-23:]:
                if item == first:
                    same += 1
            if same > 8:
                return True
        return False

    def build_cells(self):
        self.cells = [[0 for row in range(self.num_rows)] for column in range(self.num_columns)]
        for col_idx in range(self.num_columns):
            for row_idx in range(self.num_rows):
                
                self.cells[col_idx][row_idx] = Cell(self.CELL_SIZE, col_idx, row_idx)
                self.total_cells += 1

    def update(self):
        self.update_states()
        self.update_draw()
    
    def update_draw(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.update()

    def update_states(self):
        self.update_current_states()

        for cell_row in self.cells:
            for cell in cell_row:
                cell.get_neighbors(self)
                self.rule_set.apply_rules(cell)
            
        self.rule_set.add_tick()

    @jit(nopython=True)
    def update_current_states(self):
        #capture 2d bool array of current states
        self.current_states = np.zeros(shape=(self.num_rows, self.num_columns))
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                self.current_states[row, column] = self.cells[column][row].alive

    def set_rules(self, name):
        logging.info(f'Ending ruleset: {self.rule_set} after {self.rule_set.run_ticks} ticks')
        self.rule_set = Ruleset(name)
        logging.info(f'Starting ruleset: {self.rule_set}')

class Cell:
    def __init__(self, square_size, column_idx, row_idx, living=False):
        
        startx = square_size * column_idx
        starty = square_size * row_idx

        self.START_LOC = [startx, starty]

        self.column_idx = column_idx
        self.row_idx = row_idx

        red = random.randint(150, 250)
        green = random.randint(5, 25)
        blue = random.randint(green, red)
        self.color = [red, green, blue]
        self.original_color = [red, green, blue]
        self.size = [square_size, square_size]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        
        self.rect = self.surface.get_rect()
        self.rect.move_ip(self.START_LOC)

        self.alive = living
        self.neighborhood = 0

    def update(self):
        self.update_states()
        self.draw()

    def draw(self):
        main_window = pygame.display.get_surface()
        main_window.blit(self.surface, self.rect)

    def age_color(self, older=True):
        for idx, component in enumerate(self.color):
            if older:
                if component < 245:
                    self.color[idx] += 1
            else:
                if component > 20:
                    self.color[idx] -= 1
                else:
                    self.color[idx] = random.choice([self.original_color[idx], random.randint((idx + 1) * 25, (idx + 1) * 50)])
    
    def update_states(self):
        if self.alive:
            self.surface.fill(self.color)
        else:
            inverse = [255-component for component in self.color]
            self.surface.fill(inverse)

    def get_neighbors(self, grid):
        cidx = ridx = 0
        cidx  = self.column_idx
        ridx = self.row_idx
        #wrap screen
        if ridx == grid.num_rows - 1:
            rplus = 0
        else:
            rplus = ridx + 1
        if ridx == 0:
            rminus = grid.num_rows - 1
        else:
            rminus = ridx - 1
        if cidx == grid.num_columns - 1:
            cplus = 0
        else:
            cplus = cidx + 1
        if cidx == 0:
            cminus = grid.num_columns - 1
        else:
            cminus = cidx - 1

        neighbors = np.zeros(shape=(grid.num_rows, grid.num_columns), dtype=np.int8)

        #north, ne, e, se, s, sw, w, nw
        neighbors = [
            grid.current_states[rminus, cidx],
            grid.current_states[rminus, cplus],
            grid.current_states[ridx, cplus],
            grid.current_states[rplus, cplus],
            grid.current_states[rplus, cidx],
            grid.current_states[rplus, cminus],
            grid.current_states[ridx, cminus], 
            grid.current_states[rminus, cminus],
            ]

        self.neighborhood = sum(neighbors)


class Ruleset:
    def __init__(self, name):
        RULE_SETS = {
            'conway': {'survive': [2, 3], 'born': [3]},
            'amoeba': {'survive': [1, 3, 5, 8], 'born': [3, 5, 7]},
            '2x2': {'survive': [1, 2, 5], 'born': [3, 6]}, 
            '34life': {'survive': [3, 4], 'born': [3, 4]},
            'assimilation': {'survive': [4, 5, 6, 7], 'born': [3, 4, 5]},
            'coagulations': {'survive': [2, 3, 5, 6, 7, 8], 'born': [3, 7, 8]},
            'coral': {'survive': [4, 5, 6, 7, 8], 'born': [3]},
            'daynight': {'survive': [3, 4, 6, 7, 8], 'born': [3, 6, 7, 8]},
            'diamoeba': {'survive': [5, 6, 7, 8], 'born': [3, 5, 6, 7, 8]},
            'flakes': {'survive': [0, 1, 2, 3, 4, 5, 6, 7, 8], 'born': [3]}, 
            'gnarl': {'survive': [1], 'born': [1]}, 
            'highlife': {'survive': [2, 3], 'born': [3, 6]}, 
            'inverselife': {'survive': [3, 4, 6, 7, 8], 'born': [0, 1, 2, 3, 4, 7, 8]}, 
            'longlife': {'survive': [5], 'born': [3, 4, 5]},
            'maze': {'survive': [1, 2, 3, 4, 5], 'born': [3]}, 
            'mazectric': {'survive': [1, 2, 3, 4], 'born': [3]}, 
            'move': {'survive': [2, 4, 5], 'born': [3, 6, 8]},
            'pseudolife': {'survive': [2, 3, 8], 'born': [3, 5, 7]}, 
            'replicator': {'survive': [1, 3, 5, 7], 'born': [1, 3, 5, 7]}, 
            'seeds': {'survive': [], 'born': [2]}, 
            'serviettes': {'survive': [], 'born': [2, 3, 4]},
            'stains': {'survive': [2, 3, 5, 6, 7, 8], 'born': [3, 6, 7, 8]},
            'walledcities': {'survive': [2, 3, 4, 5], 'born': [4, 5, 6, 7, 8]},
        }
        self.init_time = time()
        self.name = name
        self.rule_set = RULE_SETS[self.name]
        self.run_ticks = 0
    
    def apply_rules(self, cell):
        if cell.alive:
            if cell.neighborhood not in self.rule_set['survive']:
                cell.alive = False
        else:
            if cell.neighborhood in self.rule_set['born']:
                cell.alive = True

    def add_tick(self):
        self.run_ticks += 1

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def __str__(self):
        return f'{self.name}'

class CellStamp:
    def __init__():
        pass
