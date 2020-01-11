import pygame
from MainApp import load_image, tiles_group, all_sprites


tile_images = {'background': load_image('Tileset.png')}
dicti = {}
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, sheet, columns, rows, x, y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.cut_sheet(sheet, columns, rows)
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frame_location = (self.rect.w * 60, self.rect.h * 120)

        dicti["background"] = sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))
