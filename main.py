import pygame, sys
from pygame.locals import QUIT
from objects import Player, Platform
import random
import time

pygame.mixer.pre_init(44100, 16, 2, 4096)
# pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
pygame.init()
vec = pygame.math.Vector2

HEIGHT = 360
WIDTH = 640
FPS = 60

HARD = 6

FramePerSec = pygame.time.Clock()
flags = pygame.DOUBLEBUF  # | pygame.FULLSCREEN

display_surface = pygame.display.set_mode((WIDTH, HEIGHT), flags, 16)
pygame.display.set_caption('Follow East')

background = pygame.image.load('images/background.png').convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

p1 = Player()
pt1 = Platform(w=WIDTH, h=HEIGHT)
pt1.surf = pygame.Surface((WIDTH, 20))
pt1.surf.fill((255, 0, 0))
pt1.rect = pt1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
pt1.moving = False
pt1.point = False

all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(pt1)

platforms = pygame.sprite.Group()
platforms.add(pt1)

coins = pygame.sprite.Group()

for i in range(random.randint(4, 5)):
    temp_platform = Platform(w=WIDTH, h=HEIGHT)
    temp_platform.generate_coin(coins)
    platforms.add(temp_platform)
    all_sprites.add(temp_platform)


def generate_platform():
    while len(platforms) < HARD:
        width = random.randrange(50, 100)
        flag = True
        while flag:
            p = Platform(w=WIDTH, h=HEIGHT)
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-80, 0))
            flag = check(p, platforms)
        p.generate_coin(coins)
        platforms.add(p)
        all_sprites.add(p)


def check(platform, group):
    if pygame.sprite.spritecollideany(platform, group):
        return True
    else:
        for entity in group:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) <
                    35) and (abs(platform.rect.bottom - entity.rect.top) < 35):
                return True
        return False


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                p1.jump(platforms)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                p1.cancel_jump()

    if p1.rect.top <= HEIGHT / 3:
        p1.pos.y += abs(p1.vel.y)
        for item in platforms:
            item.rect.y += abs(p1.vel.y)
            if item.rect.top >= HEIGHT:
                item.kill()
        for coin in coins:
            coin.rect.y += abs(p1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()
    if p1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        display_surface.fill((150, 150, 0))
        pygame.display.update()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    display_surface.blit(background, (0, 0))

    f = pygame.font.SysFont('Verdana', 20)
    g = f.render(str(p1.score), True, (123, 0, 255))
    display_surface.blit(g, (WIDTH / 2, 10))
    p1.update(platforms)
    generate_platform()
    for entity in all_sprites:
        if entity.rect.centery < 0:
            continue
        entity.draw(display_surface)
        # display_surface.blit(entity.surf, entity.rect)
        if isinstance(entity, Platform):
            entity.move(p1)
        else:
            entity.move()
    for coin in coins:
        display_surface.blit(coin.image, coin.rect)
        coin.update(p1)

    pygame.display.update()
    FramePerSec.tick(FPS)
