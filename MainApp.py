import pygame
from main import Block, Boss, Mob, MainScreen, Player, Board


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = screen.get_rect()[2:]
print(size)
running = True

block = Block(5, 5)
cell_size = 80
board = Board(size[0] // cell_size , size[1] // cell_size , cell_size)
player = Player(3, 3)
boss = Boss()
mob = Mob()


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
