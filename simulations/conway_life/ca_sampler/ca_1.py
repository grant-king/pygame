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

def listen(events_list, active_objs):
    #listen for and refer to handlers button presses
    for event in events_list:
        if event.type == KEYDOWN:
            if event.key == K_LCTRL:
                screenshot_handler(active_objs['capture'])
        elif event.type == SCREENSHOTEVENT:
            screenshot_handler(active_objs['capture'])
        elif event.type == GRAPHMARKEVENT:
            graphmark_handler(active_objs['graph'], active_objs['grid'])
        elif event.type == CHANGERULESETEVENT:
            changeruleset_handler(active_objs['grid'])

def screenshot_handler(capture):
    #todo add logging for past 5 routines
    capture.screen_shot()

def graphmark_handler(graph, grid):
    living = sum(grid.living_cells())
    graph.add_mark(living/10)
    
def changeruleset_handler(grid):
    rulesets = [
    'conway', 'amoeba', '2x2', '34life', 'assimilation', 'coagulations', 'coral', 
    'daynight', 'inverselife', 'longlife', 'seeds', 'serviettes',
    'maze', 'mazectric', 'move', 'pseudolife', 'replicator', 
    'stains', 'walledcities', 'diamoeba', 'flakes', 'gnarl', 'highlife',
    ]
    grid.set_rules(random.choice(rulesets))
    print(grid.rule_set.name)

    #set a couple random cells each time
    for cell_row in grid.cells[:10:2]:
        random.choice(cell_row).alive = True

def main_loop():
    pygame.init()
    
    clock = pygame.time.Clock()
    pygame.time.set_timer(SCREENSHOTEVENT, SCREENSHOT_DELAY)
    #pygame.time.set_timer(GRAPHMARKEVENT, GRAPHMARK_DELAY)
    pygame.time.set_timer(CHANGERULESETEVENT, CHANGERULESET_DELAY)

    main_window = pygame.display.set_mode(SCREEN_SIZE)
    main_window.fill(BACKGROUND_COLOR)

    graph = Graph()
    capture = Capture()

    grid = Grid(CELL_SIZE, 'gnarl')
    for cell_row in grid.cells[:10:2]:
        random.choice(cell_row).alive = True

    running = True
    while running:

        #collect, process events
        events = pygame.event.get()
        clock.tick(10)
        running = listen_quit(events)
        events_args = {'capture': capture, 'grid': grid, 'graph': graph}
        listen(events, events_args)
        
        #update and draw
        grid.update()
        living = sum(grid.living_cells())
        if living > grid.total_cells / 3:
            pygame.event.post(pygame.event.Event(SCREENSHOTEVENT))
        else:
            graph.update()

        pygame.display.flip()
        
        #check static status of grid
        if grid.check_static():
            #pygame.event.post(pygame.event.Event(CHANGERULESETEVENT))
            pass

    pygame.quit()

SCREEN_SIZE = [384, 216]
CELL_SIZE = 3
BACKGROUND_COLOR = [0, 3, 1]
CHANGE_INTERVAL = 100

SCREENSHOTEVENT = USEREVENT + 1
SCREENSHOT_DELAY = 2000

GRAPHMARKEVENT = USEREVENT + 2
GRAPHMARK_DELAY = 500

CHANGERULESETEVENT = USEREVENT + 3
CHANGERULESET_DELAY = 5 * 1000

if __name__ == '__main__':
    main_loop()
