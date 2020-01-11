import pygame, os
#from MainApp import load_image


#tile_images = {'background': load_image('Tileset.png')}
def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Can't load image:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image
#===========================

dicti = {}
tile_width = tile_height = 32
tile_images = {'wall': pygame.transform.scale(load_image('wall.jpg'), (32, 32)), 'empty': pygame.transform.scale(load_image('empty.png'), (32, 32)),
               'wizard': pygame.transform.scale(load_image('wizard.png'), (32, 32)), 'demon_boss': pygame.transform.scale(load_image('grass.png'), (32, 32)),
               'undead': pygame.transform.scale(load_image('box.png'), (32, 32)), 'knight': pygame.transform.scale(load_image('box.png'), (32, 32))}
player_image = pygame.transform.scale(load_image('mario.png'), (32, 32))

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):#, sheet, columns, rows, x, y):
        super().__init__()
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        #self.cut_sheet(sheet, columns, rows)
        #self.rect = self.rect.move(x, y)

    #def cut_sheet(self, sheet, columns, rows):
        #self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
          #                      sheet.get_height() // rows)
       # frame_location = (self.rect.w * 256, self.rect.h * 27)

       # dicti["background"] = sheet.subsurface(pygame.Rect(
       #             frame_location, self.rect.size))
