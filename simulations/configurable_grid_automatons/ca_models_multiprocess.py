import pygame
import random
import os
import logging
import numpy as np
import numba
from numba import njit, jit, int8, int32, jitclass
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

    def build_cells(self):
        self.cells = [[0 for row in range(self.num_rows)] for column in range(self.num_columns)]
        for col_idx in range(self.num_columns):
            for row_idx in range(self.num_rows):
                self.cells[col_idx][row_idx] = Cell(self.CELL_SIZE, col_idx, row_idx)
                self.total_cells += 1

    def update(self):
        self.update_states()
        self.update_cells()
    
    def update_cells(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.update()

    def update_states(self):
        self.update_current_states()
        
        for col_idx, cell_row in enumerate(self.cells):
            for row_idx, cell in enumerate(cell_row):
                # todo if first or last, wrap from edge
                if row_idx == 0 or row_idx == self.num_rows or col_idx == 0 or col_idx == self.num_columns:
                    pass    
                else:
                    neighborhood = self.get_neighborhood(row_idx, col_idx)
                    cell.set_neighbors(neighborhood)
                self.rule_set.apply_rules(cell)
            
        self.rule_set.add_tick()

    def get_neighborhood(self, row_idx, col_idx):
        #copy neighborhood surrounding cell location
        neighborhood = np.zeros(shape=(3, 3), dtype=np.bool)
        neighborhood = self.current_states[row_idx-1:row_idx+2, col_idx-1:col_idx+2].copy()
        neighborhood[1, 1] = 0
        return neighborhood

    def update_current_states(self):
        #capture 2d bool array of current states
        self.current_states = np.zeros(shape=(self.num_rows, self.num_columns), dtype=np.bool)
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                self.current_states[row, column] = self.cells[column][row].alive

    def set_rules(self, name):
        logging.info(f'Ending ruleset: {self.rule_set} after {self.rule_set.run_ticks} ticks')
        self.rule_set = Ruleset(name)
        logging.info(f'Starting ruleset: {self.rule_set}')

    def wrap_screen(self, ridx, cidx):
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

        #north, ne, e, se, s, sw, w, nw
        neighbors = [
            self.current_states[rminus, cidx],
            self.current_states[rminus, cplus],
            self.current_states[ridx, cplus],
            self.current_states[rplus, cplus],
            self.current_states[rplus, cidx],
            self.current_states[rplus, cminus],
            self.current_states[ridx, cminus], 
            self.current_states[rminus, cminus],
            ]

class Cell:
    def __init__(self, square_size, column_idx, row_idx, living=False):
        
        self.cell_logic = CellLogic(column_idx, row_idx, living=living)
        self.cell_visual = CellVisual(square_size, column_idx, row_idx, living=living)
        
    @property
    def alive(self):
        if self.cell_logic.alive:
            return True
        return False

    @property
    def neighborhood_sum(self):
        return self.cell_logic.neighborhood_sum

    def update(self):
        self.cell_visual.update()

    def set_neighbors(self, neighborhood):
        self.cell_logic.set_neighbors(neighborhood)

    def toggle_cell(self, revive=True):
        if revive:
            self.cell_logic.alive = 1
            self.cell_visual.alive = 1
        else:
            self.cell_logic.alive = 0
            self.cell_visual.alive = 0

class CellVisual:
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
        self.neighborhood_array = np.zeros(shape=(3, 3), dtype=np.bool)
        self.neighborhood_sum = 0

    def update(self):
        self.update_visual()
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
    
    def update_visual(self):
        if self.alive:
            self.surface.fill(self.color)
        else:
            inverse = [255-component for component in self.color]
            self.surface.fill(inverse)
"""
spec = [
    ('column_idx', int32),
    ('row_idx', int32), 
    ('alive' int8),
]
@jitclass
"""
class CellLogic:
    def __init__(self, column_idx, row_idx, living=False):
        self.column_idx = column_idx
        self.row_idx = row_idx

        self.alive = living
        self.neighborhood_array = np.zeros(shape=(3, 3), dtype=np.bool)
        self.neighborhood_sum = 0

    def set_neighbors(self, neighborhood_array): 
        self.neighborhood_array = neighborhood_array
        self.neighborhood_sum = int(neighborhood_array.sum())


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
            if cell.neighborhood_sum not in self.rule_set['survive']:
                cell.toggle_cell(0) #kill cell
        else:
            if cell.neighborhood_sum in self.rule_set['born']:
                cell.toggle_cell(1) #revive cell

    def add_tick(self):
        self.run_ticks += 1

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def __str__(self):
        return f'{self.name}'

        