from ca_sampler import ca_models as ca
import pygame
import random

pygame.init()
main_window = pygame.display.set_mode([1920, 1080])
grid = ca.Grid(60, 'gnarl')

for cell_row in grid.cells[:10:2]:
    random.choice(cell_row).alive = True

for tick in range(50):
    grid.update()

pygame.display.flip()

def test_set_rules():
    rulesets = [
        'conway', 'amoeba', '2x2', '34life', 'assimilation', 'coagulations', 'coral', 
        'daynight', 'inverselife', 'longlife', 'seeds', 'serviettes',
        'maze', 'mazectric', 'move', 'pseudolife', 'replicator', 
        'stains', 'walledcities', 'diamoeba', 'flakes', 'gnarl', 'highlife',
        ]
    for rule in rulesets:
        grid.set_rules(rule)
        assert  grid.rule_set == ca.Ruleset(rule)