import pygame
from pygame.locals import *
import random

class Mark(pygame.sprite.Sprite):
    def __init__(self, height, start_x):
        super(Mark, self).__init__()

        self.color = [20, 200, 30]
        self.size = [2, height]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.rect = self.surface.get_rect()
        self.rect.move_ip(start_x, 10)

    def draw(self):
        main_window = pygame.display.get_surface()
        main_window.blit(self.surface, self.rect)

    def update(self):
        self.draw()
        

class Graph:
    def __init__(self):
        self.MAX_X = pygame.display.get_surface().get_size()[0]
        self.marks = [Mark(1, 10)]

    def update(self):
        for mark in self.marks:
            mark.update()
            if mark.rect.x > self.MAX_X:
                self.marks.remove(mark)

    def add_mark(self, new_mark_size):
        for mark in self.marks:
            mark.rect.move_ip(10, 0)
        self.marks.append(Mark(new_mark_size, 10))


class Cell(pygame.sprite.Sprite):
    def __init__(self, square_size, column_idx, row_idx, living=False):
        super(Cell, self).__init__()
        
        startx = square_size * column_idx
        starty = square_size * row_idx

        self.START_LOC = [startx, starty]

        self.column_idx = column_idx
        self.row_idx = row_idx

        red = random.randint(10, 200)
        blue = random.randint(10, 200)
        self.color = [red, abs(red-blue), blue]
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

    def update_states(self):
        if self.alive:
            self.surface.fill(self.color)
        else:
            self.surface.fill([0, 0, 0])

    
class Grid:
    def __init__(self, cell_size, rule_name):
        self.SCREEN_SIZE = pygame.display.get_surface().get_size()
        self.CELL_SIZE = cell_size

        self.cells = []
        self.cells_history = [] #list of sum of bools state history
        self.num_columns = self.SCREEN_SIZE[0] // self.CELL_SIZE
        self.num_rows = self.SCREEN_SIZE[1] // self.CELL_SIZE
        self.current_states = [[]]
        self.rule_set = Ruleset(rule_name)
        self.build_cells()

    @property        
    def static(self):
        if len(self.cells_history) > 24:
            first = self.cells_history[-24]
            same = 0
            for item in self.cells_history[-23:]:
                if item == first:
                    same += 1
            if same > 8:
                return True
        return False

    def living_cells(self):
        live_cells = []
        for cell_row in self.cells:
            for cell in cell_row:
                live_cells.append(cell.alive)
        return live_cells

    def build_cells(self):
        self.cells = [[0 for row in range(self.num_rows)] for column in range(self.num_columns)]
        for col_idx in range(self.num_columns):
            for row_idx in range(self.num_rows):
                
                self.cells[col_idx][row_idx] = Cell(self.CELL_SIZE, col_idx, row_idx)

    def update(self):
        self.update_states()
        self.update_draw()
    
    def update_draw(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.update()

    def update_states(self):
        #capture 2d bool array of current states
        self.current_states = [[0 for row in range(self.num_rows)] for column in range(self.num_columns)]
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                self.current_states[column][row] = self.cells[column][row].alive

        self.cells_history.append(self.sum_states())

        for cell_row in self.cells:
            for cell in cell_row:
                neighbors = self.get_neighbors(cell)
                cell.neighborhood = sum(neighbors)

                #self.conway_rules(cell)
                self.rule_set.apply_rules(cell)
    
    def sum_states(self):
        total = 0
        for cell_row in self.current_states:
            for cell in cell_row:
                total += cell
        return total

    def set_rules(self, name):
        self.rule_set = Ruleset(name)
    
    def get_neighbors(self, cell):
        cidx, ridx = cell.column_idx, cell.row_idx
        #wrap screen
        if ridx == self.num_rows - 1:
            rplus = 0
        else:
            rplus = ridx + 1
        if ridx == 0:
            rminus = self.num_rows - 1
        else:
            rminus = ridx - 1
        if cidx == self.num_columns - 1:
            cplus = 0
        else:
            cplus = cidx + 1
        if cidx == 0:
            cminus = self.num_columns - 1
        else:
            cminus = cidx - 1

        #north, ne, e, se, s, sw, w, nw
        neighbors = [
            self.current_states[cidx][rminus],
            self.current_states[cplus][rminus],
            self.current_states[cplus][ridx],
            self.current_states[cplus][rplus],
            self.current_states[cidx][rplus],
            self.current_states[cminus][rplus],
            self.current_states[cminus][ridx], 
            self.current_states[cminus][rminus],
            ]

        return neighbors


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
            'walledcities': {'survive': [2, 3, 4, 5], 'born': [4, 5, 6, 7, 8]}
        }
        self.name = name
        self.rule_set = RULE_SETS[self.name]

    def apply_rules(self, cell):
        if cell.alive:
            if cell.neighborhood not in self.rule_set['survive']:
                cell.alive = False
        else:
            if cell.neighborhood in self.rule_set['born']:
                cell.alive = True        


