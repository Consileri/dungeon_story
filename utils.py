import pygame, os


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Can't load image:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


WIDTH_BOSS = 3
HEIGHT_BOSS = 3
WIDTH_GG = 1
HEIGHT_GG = 2

tile_width = tile_height = 32

MOVE_SPEED = 2
FPS = 60
JUMP_POWER = 10
GRAVITY = 0.35

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

die = False
hp_hero = 10  # жизни героя
hp_boss = 20  # жизни босса
hp_mob = 2  # жизни моба

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

WHITE = pygame.Color('white')
GREEN = pygame.Color('green')

player_image = pygame.transform.scale(load_image('mario.png'), (32, 32))


class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surf):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                left = self.left + j * self.cell_size
                top = self.top + i * self.cell_size
                rect = pygame.Rect((left, top), (self.cell_size,) * 2)
                width = 0 if cell else 1
                pygame.draw.rect(surf, (255, 255, 255), rect, width)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x1 = (x - self.left) // self.cell_size
        if x1 < 0 or x1 >= self.width:
            return None

        y1 = (y - self.left) // self.cell_size
        if y1 < 0 or y1 >= self.height:
            return None

        return x1, y1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # находится ли герой на поверхности
        self.contact = False
        self.jump = JUMP_POWER
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:                       # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:                       # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:                       # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True           # и становится на что-то твердое
                    self.yvel = 0                  # и энергия падения пропадает

                if yvel < 0:                       # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0                  # и энергия прыжка пропадает

    # def die(self):
    #     global die
    #     if hp_hero <= 0:
    #         die = True
    #     pygame.time.wait(500)
    #     game_over()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Mob(pygame.sprite.Sprite):  # todo класс мобов
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, pyganim=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 6))
        self.image.fill(pygame.Color('black'))
        self.rect = pygame.Rect(x, y, 5, 6)
        self.image.set_colorkey(pygame.Color('black'))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = left
        self.yvel = up
        boltAnim = []
        # for anim in ANIMATION_MONSTERHORYSONTAL:
        #     boltAnim.append((anim, 0.3))
        # self.boltAnim = pyganim.PygAnimation(boltAnim)
        # self.boltAnim.play()

    def update(self, platforms):  # по принципу героя

        self.image.fill(pygame.Color('black'))  # бета-версия цвета моба
        # self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = -self.xvel
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel

    def die(self):
        pass


class Boss(Mob):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, pyganim=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 6))
        self.image.fill(pygame.Color('black'))
        self.rect = pygame.Rect(x, y, 5, 6)
        self.image.set_colorkey(pygame.Color('black'))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = left
        self.yvel = up
        # здесь будет анимация

    def update(self, platforms):
        self.image.fill(pygame.Color('black'))  # бета-версия цвета моба
        # self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = -self.xvel
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
