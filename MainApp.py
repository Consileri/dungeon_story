import pygame


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)



running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

         #Выход при нажатии Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
         #Пробел
        if event.type == pygame.KEYDOWN:
            if event.unicode == ' ':
                pass
         #W
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass
         #A
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pass
         #D
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                pass

    pygame.display.flip()