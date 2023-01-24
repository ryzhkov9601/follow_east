import pygame, random

vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
JUMP = -16

# ниже вписать имя файла картинки персонажа
CHARACTER_NAME = 'fairy_king_sideview3'


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            f'images/{CHARACTER_NAME}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        # self.surf = pygame.Surface((30, 30))
        # self.surf.fill((128, 255, 40))
        # self.rect = self.image.get_rect()
        self.rect = pygame.Surface((60, 60)).get_rect()

        self.pos = vec((50, 350))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.view_direction = pygame.K_RIGHT
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
            self.view_direction = pygame.K_LEFT
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC
            self.view_direction = pygame.K_RIGHT

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = JUMP

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def draw(self, surface):
        if self.view_direction == pygame.K_RIGHT:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(pygame.transform.flip(self.image.copy(), True, False),
                         self.rect)


class Platform(pygame.sprite.Sprite):

    def __init__(self, w, h):
        super().__init__()
        random_width = random.randint(50, 100)
        random_center = (random.randint(0, w - 10), random.randint(0, h - 30))
        self.image = pygame.image.load('images/tile_wood.png')
        self.surf = pygame.transform.scale(self.image, (random_width, 12))
        # self.surf = pygame.Surface((random_width, 12))
        # self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=random_center)
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.point = True

    def generate_coin(self, coins):
        if self.speed == 0:
            coins.add(Coin(pos=(self.rect.centerx, self.rect.centery - 50)))

    def move(self, player):
        hits = self.rect.colliderect(player.rect)
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if hits:
                player.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def draw(self, surface):
        surface.blit(self.surf, self.rect)


class Coin(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load('images/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.score += 5
            self.kill()
