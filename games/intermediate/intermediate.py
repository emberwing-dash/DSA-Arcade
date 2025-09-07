import pygame
from dora import Dora

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Intermediate Level - Dora Test")

clock = pygame.time.Clock()

# Create Dora instance
dora = Dora(screen, "assets", pos=(100, 400))

running = True
while running:
    screen.fill((150, 200, 250))  # background sky blue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        dora.walk("right")
    elif keys[pygame.K_LEFT]:
        dora.walk("left")
    else:
        dora.idle()

    # Update + Draw Dora
    dora.update()
    dora.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
