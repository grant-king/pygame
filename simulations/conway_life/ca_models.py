import pygame
from pygame.locals import *
import random

class Cell(pygame.sprite.Sprite):
    def __init__(self, square_size, column_idx, row_idx, living=False):
        super(Cell, self).__init__()
        
        startx = square_size * column_idx
        starty = square_size * row_idx

        self.START_LOC = [startx, starty]

        self.column_idx = column_idx 
        self.row_idx = row_idx

        blue = random.randint(90, 110)
        self.color = [255-blue, 80, blue]
        self.size = [square_size, square_size]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        
        self.rect = self.surface.get_rect()
        self.rect.move_ip(self.START_LOC)

        self.alive = living

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
    def __init__(self, cell_size):
        self.SCREEN_SIZE = pygame.display.get_surface().get_size()
        self.CELL_SIZE = cell_size

        self.cells = []
        self.num_columns = self.SCREEN_SIZE[0] // self.CELL_SIZE
        self.num_rows = self.SCREEN_SIZE[1] // self.CELL_SIZE
        self.current_states = []
        self.build_cells()

    def build_cells(self):
        self.cells = [[0 for row in range(self.num_rows)] for column in range(self.num_columns)]
        for col_idx in range(self.num_columns):
            for row_idx in range(self.num_rows):
                self.cells[col_idx][row_idx] = Cell(self.CELL_SIZE, col_idx, row_idx, random.choice([True, False]))
    
    def get_cell(self, col_idx, row_idx):
        for cell in self.cells:
            if cell.column_idx == col_idx and cell.row_idx == row_idx:
                    return cell

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

        for cell_row in self.cells:
            for cell in cell_row:
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

                neighborhood = sum(neighbors)
                if cell.alive:
                    if neighborhood < 2 or neighborhood > 3:
                        cell.alive = False
                else:
                    if neighborhood == 3:
                        cell.alive = True






        

