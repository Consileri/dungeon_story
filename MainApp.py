import pygame
from main import Block, Boss, Mob, Player, Board

COLUMS = 33
ROWS = 256
CELL_CIZE = 32

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
    nametext = ['Dungeon story']

    background = pygame.transform.scale(load_image('fon.jpg'), (1920, 1080))
    screen.blit(background, (0, 0))
    intro_font = pygame.font.Font(None, 75)
    name_font = pygame.font.Font(None, 125)
    text_coord = 975
    name_coord = 50

    name_rendered = name_font.render(nametext[0], 1, TEXTCOLOR)
    name_rect = name_rendered.get_rect()
    name_coord += 10
    name_rect.top = name_coord
    name_rect.x = 680
    name_coord += name_rect.height
    screen.blit(name_rendered, name_rect)

    for line in introtext:
        string_rendered = intro_font.render(line, 1, TEXTCOLOR)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 410
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
board = Board(size[0] // cell_size , size[1] // cell_size , cell_size)
player = Player(3, 3)
boss = Boss()
mob = Mob()


while running:
    screen.fill(BACKGROUNDCOLOR)
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
