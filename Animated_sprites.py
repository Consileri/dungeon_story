import pygame
from MainApp import load_image

all_sprites = pygame.sprite.Group()

class AnimatedSpriteDemon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        frames =  self.cut_sheet(load_image('demon_attack.png'), 4, 4)

        self.frames = {
            #'bottom': self.frames[:4],
            #'top': self.frames[4:8],
            'attack_right': frames[8:12],
            'attack_left': frames[12:],
            'idle' : frames[3:4]
        }
        frames = self.cut_sheet(load_image('demon_death.png'), 7, 1)
        self.frames['death'] = frames
        frames = self.cut_sheet(load_image('demon_walk.png'), 4, 4)
        self.frames['walk_right'] = frames[8:12]
        self.animation = 'walk_left'
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        result = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                result.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return result
    def update(self):
        if self.animation == 'death' and self.cur_frame == 6:
            self.kill()
            return
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.animation])
        self.image = self.frames[self.animation][self.cur_frame]

    def move_left(self):
        self.cur_frame = 0
        self.animation = 'walk_left'

    def move_right(self):
        self.cur_frame = 0
        self.animation = 'walk_right'

    def attack_right(self):
        self.cur_frame = 0
        self.animation = 'attack_right'

    def attack_left(self):
        self.cur_frame = 0
        self.animation = 'attack_left'

    def idle(self):
        self.cur_frame = 0
        self.animation = 'idle'


class AnimatedSpriteKnight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        frames = self.cut_sheet(load_image('knight_slash.png'), 4, 4)

        self.frames = {
            'attack_right' : frames,
            'attack_left' : list(map(lambda surface: pygame.transform.flip(surface, True, False)))
        }

        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        result = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                result.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return result

    def update(self):
        if self.animation == 'death' and self.cur_frame == 6:
            self.kill()
            return
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.animation])
        self.image = self.frames[self.animation][self.cur_frame]








