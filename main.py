import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 50

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


pygame.init()
size = width, height = 1000, 1000
surf = pygame.display.set_mode(size)

board = Board(5, 7)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board.get_cell(event.pos))
    surf.fill((0, 0, 0))
    board.render(surf)
    pygame.display.flip()