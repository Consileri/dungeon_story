import pygame, sys, os
from main import Block, Boss, Mob, Player, Board

COLUMS = 26
ROWS = 256
CELL_CIZE = 40

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
size = width, height = screen.get_rect()[2:]
print(size)

clock = pygame.time.Clock()
WIDTH_BOSS = 4
HEIGHT_BOSS = 2
WIDTH_GG = 1
HEIGHT_GG = 2
MOVE_SPEED = 2
FPS = 60

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Can't load image:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def main_screen():  # todo класс заставки
    introtext = ['Чтобы начать игру, '
                 'Нажмите любую кнопку']

    background = pygame.transform.scale(load_image('fon.jpg'), (1920, 1080))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in introtext:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 770
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)

running = True

block = Block(5, 5)
cell_size = 80
board = Board(ROWS, COLUMS, CELL_CIZE)
player = Player(3, 3)
boss = Boss()
mob = Mob(5, 6)

main_screen()
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Выход при нажатии Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # Пробел
        if event.type == pygame.KEYDOWN:
            if event.unicode == ' ':
                pass
        # W
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass
        # A
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pass
        # D
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                pass
    board.render(screen)
    pygame.display.flip()
