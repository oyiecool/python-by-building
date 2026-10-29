class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 210, 0), (8, 8), 8)
        self.rect = self.image.get_rect(center=(x, y))

coins = pygame.sprite.Group(Coin(100, 100), Coin(200, 150))
collected = pygame.sprite.spritecollide(player_sprite, coins, dokill=True)
