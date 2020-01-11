import pygame, sys, os
from main import Platform, Boss, Mob, Player, Board
from random import choice


COLUMS = 33
ROWS = 256
CELL_CIZE = 32

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
BACKGROUNDCOLOR = pygame.Color(64, 32, 0)
TEXTCOLOR = pygame.Color(218, 189, 171)
TILE_WIDTH = 32
TILE_HEIGHT = 32
FONT = 'agencyfb'
left = False
up = False
right = False
platforms = []

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
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
    nametext = ['Dungeon story']

    background = pygame.transform.scale(load_image('fon.jpg'), (1920, 1080))
    screen.blit(background, (0, 0))
    intro_font = pygame.font.Font(None, 50)
    name_font = pygame.font.SysFont(FONT, 150)
    text_coord = 1000
    name_coord = 50

    name_rendered = name_font.render(nametext[0], 1, TEXTCOLOR)
    name_rect = name_rendered.get_rect()
    name_coord += 10
    name_rect.top = name_coord
    name_rect.x = (1920 - name_rect.width) // 2
    name_coord += name_rect.height
    screen.blit(name_rendered, name_rect)

    for line in introtext:
        string_rendered = intro_font.render(line, 1, TEXTCOLOR)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (1920 - intro_rect.width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(FPS)

def game_menu():
    exit_text = ['Выход']
    continue_text = ['Продолжить']

    background = pygame.transform.scale(load_image(choice(['menu.jpg', 'real_menu.jpg', 'real_menu.jpg', 'real_menu.jpg', 'real_menu.jpg'])), (1920, 1080))
    screen.blit(background, (0, 0))
    exit_font = pygame.font.Font(None, 100)
    continue_font = pygame.font.Font(None, 100)
    exit_coord = 600
    continue_coord = 400

    exit_rendered = exit_font.render(exit_text[0], 1, TEXTCOLOR)
    exit_rect = exit_rendered.get_rect()
    exit_coord += 10
    exit_rect.top = exit_coord
    exit_rect.x = (1920 - exit_rect.width) // 2
    exit_coord += exit_rect.height
    screen.blit(exit_rendered, exit_rect)

    continue_rendered = continue_font.render(continue_text[0], 1, TEXTCOLOR)
    continue_rect = continue_rendered.get_rect()
    continue_coord += 10
    continue_rect.top = continue_coord
    continue_rect.x = (1920 - continue_rect.width) // 2
    continue_coord += continue_rect.height
    screen.blit(continue_rendered, continue_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if (pos[0] > exit_rect.x and pos[0] < (exit_rect.width + exit_rect.x)) and (pos[1] > exit_rect.y and pos[1] < (exit_rect.height + exit_rect.y)):
                    terminate()
                elif (pos[0] > continue_rect.x and pos[0] < (continue_rect.width + continue_rect.x)) and (pos[1] > continue_rect.y and pos[1] < (continue_rect.height + continue_rect.y)):
                    return
        pygame.display.flip()
        clock.tick(FPS)

running = True

plat = Platform(5, 5)
cell_size = 80
board = Board(ROWS, COLUMS, CELL_CIZE)
player = Player(3, 3)
boss = Boss(0, 0)
mob = Mob(5, 6, 0, 0, 0, 0)


main_screen()
while running:
    screen.fill(BACKGROUNDCOLOR)
    player.update(left, right, up, platforms)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Выход при нажатии Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_menu()
        # Пробел
        if event.type == pygame.KEYDOWN:
            if event.unicode == ' ':
                pass
        # W
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = True
                right = False
                left = False
        # A
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                up = False
                right = False
                left = True
        # D
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                up = False
                right = True
                left = False
    board.render(screen)
    pygame.display.flip()
