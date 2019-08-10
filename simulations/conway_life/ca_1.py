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

pygame.init()
main_window = pygame.display.set_mode(SCREEN_SIZE)
main_window.fill(BACKGROUND_COLOR)

grid = Grid(CELL_SIZE)

running = True
clock = pygame.time.Clock()
draw_cell = 0

while running:
    events = pygame.event.get()
    clock.tick(10)
    running = listen_quit(events)
    
    #update and draw

    grid.update()
    pygame.display.flip()

pygame.quit()
