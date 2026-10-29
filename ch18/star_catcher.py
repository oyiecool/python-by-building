# star_catcher.py
import json, random
from pathlib import Path
import pygame

WIDTH, HEIGHT = 640, 480
HS_FILE = Path(__file__).resolve().parent / "highscore.json"
BG, WHITE, GOLD, RED, BLUE = (18, 22, 36), (240, 240, 240), (255, 205, 40), (230, 70, 70), (80, 170, 255)

def load_high() -> int:
    try:
        return json.loads(HS_FILE.read_text())["high"]
    except (FileNotFoundError, KeyError, ValueError):
        return 0

def save_high(score: int):
    HS_FILE.write_text(json.dumps({"high": score}))

class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((90, 22), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLUE, self.image.get_rect(), border_radius=8)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 12))
        self.speed = 480

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.rect.x += round(dx * self.speed * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

class Falling(pygame.sprite.Sprite):
    def __init__(self, kind: str, speed: float):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        color = GOLD if kind == "star" else RED
        pygame.draw.circle(self.image, color, (11, 11), 11)
        if kind == "bomb":
            pygame.draw.line(self.image, WHITE, (11, 0), (16, -4), 2)
        self.rect = self.image.get_rect(midbottom=(random.randint(15, WIDTH - 15), 0))
        self.y = float(self.rect.y)
        self.speed = speed * random.uniform(0.8, 1.3)

    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = round(self.y)
        if self.rect.top > HEIGHT:
            self.kill()                       # remove from all groups

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Star Catcher")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.big = pygame.font.SysFont("consolas", 48, bold=True)
        self.high = load_high()
        self.state = "title"
        self.reset()

    def reset(self):
        self.basket = Basket()
        self.items = pygame.sprite.Group()
        self.score, self.lives, self.spawn_timer = 0, 3, 0.0

    @property
    def level(self) -> int:
        return 1 + self.score // 10

    def spawn(self, dt):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            kind = "bomb" if random.random() < min(0.15 + 0.03 * self.level, 0.45) else "star"
            self.items.add(Falling(kind, 140 + 25 * self.level))
            self.spawn_timer = max(0.25, 0.9 - 0.06 * self.level)

    def play(self, dt):
        self.basket.update(dt)
        self.spawn(dt)
        self.items.update(dt)
        for item in pygame.sprite.spritecollide(self.basket, self.items, dokill=True):
            if item.kind == "star":
                self.score += 1
            else:
                self.lives -= 1
                if self.lives == 0:
                    if self.score > self.high:
                        self.high = self.score
                        save_high(self.high)
                    self.state = "over"

    def text(self, msg, font, color, center):
        surf = font.render(msg, True, color)
        self.screen.blit(surf, surf.get_rect(center=center))

    def draw(self):
        self.screen.fill(BG)
        if self.state == "title":
            self.text("STAR CATCHER", self.big, GOLD, (WIDTH // 2, 170))
            self.text("Arrows or A/D to move. Catch stars, dodge bombs.", self.font, WHITE, (WIDTH // 2, 250))
            self.text("Press SPACE to start", self.font, BLUE, (WIDTH // 2, 300))
        else:
            self.items.draw(self.screen)
            self.screen.blit(self.basket.image, self.basket.rect)
            hud = f"Score {self.score}   Lives {'♥' * self.lives}   Level {self.level}   Best {self.high}"
            self.screen.blit(self.font.render(hud, True, WHITE), (10, 8))
            if self.state == "paused":
                self.text("PAUSED (P)", self.big, WHITE, (WIDTH // 2, HEIGHT // 2))
            if self.state == "over":
                self.text("GAME OVER", self.big, RED, (WIDTH // 2, 190))
                self.text(f"Score {self.score}  -  SPACE to play again", self.font, WHITE, (WIDTH // 2, 250))
        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.state in ("title", "over"):
                    self.reset()
                    self.state = "playing"
                if e.type == pygame.KEYDOWN and e.key == pygame.K_p and self.state in ("playing", "paused"):
                    self.state = "paused" if self.state == "playing" else "playing"
            if self.state == "playing":
                self.play(dt)
            self.draw()

if __name__ == "__main__":
    Game().run()
