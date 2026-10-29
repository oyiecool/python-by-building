pygame.draw.circle(screen, (255, 200, 0), (320, 240), 30)
pygame.draw.line(screen, (255, 255, 255), (0, 400), (640, 400), 2)
pygame.draw.polygon(screen, (0, 200, 120), [(100, 100), (140, 180), (60, 180)])

font = pygame.font.SysFont("consolas", 28)
text = font.render("Score: 10", True, (255, 255, 255))   # True = smooth edges
screen.blit(text, (10, 10))
