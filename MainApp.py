import pygame
from main import Block, Boss, Mob, Player, Board

COLUMS = 26
ROWS = 256
CELL_CIZE = 40

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
size = width, height = screen.get_rect()[2:]
print(size)
running = True

block = Block(5, 5)
cell_size = 80
board = Board(ROWS, COLUMS, CELL_CIZE)
player = Player(3, 3)
boss = Boss()
mob = Mob(5, 6)


while running:
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
