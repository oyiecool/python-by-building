import random
import pygame

W, H, SPEED = 800, 500, 420

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pong")
    clock, font = pygame.time.Clock(), pygame.font.SysFont("consolas", 40)
    left, right = pygame.Rect(20, H // 2 - 50, 12, 100), pygame.Rect(W - 32, H // 2 - 50, 12, 100)
    ball = pygame.Rect(W // 2 - 8, H // 2 - 8, 16, 16)
    vx, vy = random.choice([-1, 1]) * 300, random.uniform(-200, 200)
    bx, by = float(ball.x), float(ball.y)
    score = [0, 0]
    while True:
        dt = clock.tick(60) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        keys = pygame.key.get_pressed()
        left.y += round((keys[pygame.K_s] - keys[pygame.K_w]) * SPEED * dt)
        right.y += round((keys[pygame.K_DOWN] - keys[pygame.K_UP]) * SPEED * dt)
        left.clamp_ip(screen.get_rect())
        right.clamp_ip(screen.get_rect())

        bx += vx * dt
        by += vy * dt
        ball.topleft = (round(bx), round(by))
        if ball.top <= 0 or ball.bottom >= H:            # bounce off top/bottom
            vy = -vy
            by = max(0, min(by, H - ball.height))
        for paddle in (left, right):
            if ball.colliderect(paddle) and (vx < 0) == (paddle is left):
                vx = -vx * 1.05                           # speed up a little each hit
                vy += (ball.centery - paddle.centery) * 4 # angle depends on where it hits
        if ball.right < 0 or ball.left > W:               # a point is scored
            score[0 if ball.left > W else 1] += 1
            bx, by = W / 2 - 8, H / 2 - 8
            vx, vy = (300 if vx < 0 else -300), random.uniform(-200, 200)

        screen.fill((15, 18, 30))
        pygame.draw.aaline(screen, (80, 80, 100), (W // 2, 0), (W // 2, H))
        for r in (left, right):
            pygame.draw.rect(screen, (230, 230, 230), r)
        pygame.draw.ellipse(screen, (255, 205, 40), ball)
        text = font.render(f"{score[0]}   {score[1]}", True, (230, 230, 230))
        screen.blit(text, text.get_rect(midtop=(W // 2, 12)))
        pygame.display.flip()

if __name__ == "__main__":
    main()
