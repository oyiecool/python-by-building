import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Moving square")
clock = pygame.time.Clock()

x, y, speed = 300, 220, 300          # speed in pixels per second
running = True
while running:
    dt = clock.tick(60) / 1000       # cap at 60 FPS; dt = seconds since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  x -= speed * dt
    if keys[pygame.K_RIGHT]: x += speed * dt
    if keys[pygame.K_UP]:    y -= speed * dt
    if keys[pygame.K_DOWN]:  y += speed * dt
    x = max(0, min(x, 640 - 40))     # keep on screen
    y = max(0, min(y, 480 - 40))

    screen.fill((20, 24, 35))
    pygame.draw.rect(screen, (80, 170, 255), (x, y, 40, 40))
    pygame.display.flip()

pygame.quit()
