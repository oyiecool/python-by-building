player = pygame.Rect(300, 420, 50, 20)
coin = pygame.Rect(310, 100, 16, 16)
if player.colliderect(coin):
    print("collected!")
player.centerx = 320           # move by any edge or centre
player.clamp_ip(screen.get_rect())   # keep inside the screen
