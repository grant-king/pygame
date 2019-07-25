from sim_models import *


def listen_quit(events_list):
    #listen for quit
    for event in events_list:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
        elif event.type == QUIT:
            return False
    return True

SCREEN_SIZE = [1280, 720]
BACKGROUND_COLOR = [0, 3, 1]

SOFTNER_SURF = pygame.Surface(SCREEN_SIZE)
SOFTNER_SURF.set_alpha(1)
SOFTNER_SURF.fill(BACKGROUND_COLOR)

pygame.init()
main_window = pygame.display.set_mode(SCREEN_SIZE)
main_window.fill(BACKGROUND_COLOR)

particles = [Particle() for item in range(500)]

running = True
clock = pygame.time.Clock()
clear_tick = 0

while running:
    events = pygame.event.get()
    #clock.tick(200)
    
    
    running = listen_quit(events)

    for particle in particles:
        x, y = particle.rect.x, particle.rect.y
        if x > particle.max_x or x < 0 or y > particle.max_y or y < 0:
            #particles.pop(particles.index(particle))
            #print(f'particle {particle} removed\n {len(particles)} particles in list')
            particle.recenter()
            #soften slightliy with each particle loss
            main_window.blit(SOFTNER_SURF, (0, 0))

            

    for particle in particles:
        particle.update(events)

    pygame.display.flip()

pygame.quit()
