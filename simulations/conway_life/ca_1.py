from ca_models import *
import os

def listen_quit(events_list):
    #listen for quit
    for event in events_list:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
        elif event.type == QUIT:
            return False
    return True

def listen(events_list):
    #listen for and refer to handlers button presses
    for event in events_list:
        if event.type == KEYDOWN:
            if event.key == K_LCTRL:
                screenshot_handler()
        elif event.type == SCREENSHOTEVENT:
            screenshot_handler()

def screenshot_handler():
    capture.screen_shot()


SCREEN_SIZE = [384, 216]
CELL_SIZE = 3
BACKGROUND_COLOR = [0, 3, 1]
CHANGE_INTERVAL = 100

pygame.init()

SCREENSHOTEVENT = USEREVENT + 1
SCREENSHOT_DELAY = 2000

clock = pygame.time.Clock()
pygame.time.set_timer(SCREENSHOTEVENT, SCREENSHOT_DELAY)
main_window = pygame.display.set_mode(SCREEN_SIZE)
main_window.fill(BACKGROUND_COLOR)

graph = Graph()
capture = Capture()

running = True
static = False
rulesets = [
    'conway', 'amoeba', '2x2', '34life', 'assimilation', 'coagulations', 'coral', 
    'daynight', 'inverselife', 'longlife', 'seeds', 'serviettes',
    'maze', 'mazectric', 'move', 'pseudolife', 'replicator', 
    'stains', 'walledcities', 'diamoeba', 'flakes', 'gnarl', 'highlife',
    ]

rule_tracker = -2
new_mark = 0

grid = Grid(CELL_SIZE, 'conway')
while running:
    change_counter = 0
    
    print(rulesets[rule_tracker])
    grid.set_rules(rulesets[rule_tracker])

    #set a couple random cells each time
    for cell_row in grid.cells[:10:2]:
        random.choice(cell_row).alive = True

    while not static:
        events = pygame.event.get()
        clock.tick(10)
        running = listen_quit(events)
        listen(events)
        
        #update and draw
        grid.update()
        #graph.update()

        pygame.display.flip()

        living = sum(grid.living_cells())
        #add new mark to graph every so often
        
        if new_mark > 5:
            new_mark = 0
            graph.add_mark(living/10)
        new_mark += 1

        if living > grid.total_cells / 3:
            pygame.event.post(pygame.event.Event(SCREENSHOTEVENT))

        #check static status
        static = grid.static
        change_counter += 1
        if change_counter > CHANGE_INTERVAL:
            static = True

    static = False
    rule_tracker = random.randrange(len(rulesets))

pygame.quit()
