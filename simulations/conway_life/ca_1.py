from ca_models import *

def listen_quit(events_list):
    #listen for quit
    for event in events_list:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
        elif event.type == QUIT:
            return False
    return True

SCREEN_SIZE = [1920, 1080]
CELL_SIZE = 15
BACKGROUND_COLOR = [0, 3, 1]
CHANGE_INTERVAL = 300

pygame.init()
main_window = pygame.display.set_mode(SCREEN_SIZE)
main_window.fill(BACKGROUND_COLOR)

graph = Graph()

running = True
static = False
rulesets = [
    'conway', 'amoeba', '2x2', '34life', 'assimilation', 'coagulations', 'coral', 
    'daynight', 'diamoeba', 'flakes', 'gnarl', 'highlife', 'inverselife', 'longlife',
    'maze', 'mazectric', 'move', 'pseudolife', 'replicator', 'seeds', 'serviettes',
    'stains', 'walledcities'
    ]
rule_tracker = random.randint(0, len(rulesets))
clock = pygame.time.Clock()
new_mark = 0

grid = Grid(CELL_SIZE, 'gnarl')
while running:
    change_counter = 0
    if rule_tracker >= len(rulesets):
        rule_tracker = 0

    #set a couple random cells each time
    for cell_row in random.choices(grid.cells, k=1):
        for cell in random.choices(cell_row, k=2):
            cell.alive = True

    while not static:
        events = pygame.event.get()
        clock.tick(10)
        running = listen_quit(events)
        
        #update and draw
        grid.update()
        graph.update()

        pygame.display.flip()

        #add new mark to graph every so often
        if new_mark > 4:
            new_mark = 0
            living = sum(grid.living_cells())
            graph.add_mark(living/10)
        new_mark += 1

        #check static status
        static = grid.static
        change_counter += 1
        if change_counter > CHANGE_INTERVAL:
            static = True

    grid.set_rules(rulesets[rule_tracker])
    print(rulesets[rule_tracker])

    rule_tracker += 1
    static = False
    

pygame.quit()
