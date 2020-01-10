import pygame

WIDTH_BOSS = 3
HEIGHT_BOSS = 3
WIDTH_GG = 1
HEIGHT_GG = 2
MOVE_SPEED = 2
FPS = 60
JUMP = True

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.contact = False
        self.jump = JUMP
        self.image = pygame.Surface((WIDTH_GG, HEIGHT_GG))
        self.image.fill(pygame.Color('yellow'))
        self.rect = pygame.Rect(x, y, WIDTH_GG, HEIGHT_GG)

    def update(self, left, right, up):
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if up:
            if self.contact:
                self.jump = True
                self.yvel -= 4

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel

        if self.jump:
            self.yvel += 2
            self.rect.top += self.yvel


    def draw(self, screen):  # выводим на экран героя
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Block:
    def __init__(self, x, y):
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((WIDTH_GG, 1))
        self.image.fill(pygame.Color('brown'))
        self.rect = pygame.Rect(x, y, WIDTH_GG, 1)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Mob(pygame.sprite.Sprite):  # todo класс мобов
    def __init__(self, x, y):
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((1, 2))

    def update(self):  # todo функцию перемещения мобов
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Boss(pygame.sprite.Sprite):  # todo класс босса
    def __init__(self, x, y):
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((WIDTH_BOSS, HEIGHT_BOSS))

    def update(self):  # todo функцию перемещения босса
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
