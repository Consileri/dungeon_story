import pygame, os

MOVE_SPEED = 15
JUMP_POWER = 10
GRAVITY = 0.35
tile_width = tile_height = 64

all_sprites = pygame.sprite.Group()

def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Can't load image:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.count = 0

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

    def death(self):
        self.cur_frame = 0
        self.animation = 'death'

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
        n = len(self.frames[self.animation])
        if self.count % 50 == 0:
            self.cur_frame += 1
            if self.animation == 'death_right' or self.animation == 'death_left' and self.cur_frame == n:
                self.kill()
                return
            self.cur_frame = self.cur_frame % n
            self.image = self.frames[self.animation][self.cur_frame]
        self.count += 1

class AnimatedSpriteDemon(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        frames =  self.cut_sheet(load_image('Sprite_sheets/Demon_Boss/demon_attack.png'), 4, 4)

        self.frames = {
            #'bottom': self.frames[:4],
            #'top': self.frames[4:8],
            'attack_right': frames[8:12],
            'attack_left': frames[12:],
            'idle' : frames[3:4],
        }
        frames = self.cut_sheet(load_image('Sprite_sheets/Demon_Boss/demon_death.png'), 7, 1)
        self.frames['death_right'] = frames
        self.frames['death_left'] = frames

        frames = self.cut_sheet(load_image('Sprite_sheets/Demon_Boss/demon_walk.png'), 4, 4)
        self.frames['walk_right'] = frames[8:12]
        self.frames['walk_left'] = frames[12:16]
        self.animation = 'walk_left'
        self.cur_frame = 0
        self.image = self.frames[self.animation][self.cur_frame]
        self.rect = self.rect.move(x * tile_width, y * tile_width)


class AnimatedSpriteKnight(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        frames = self.cut_sheet(load_image('Sprite_sheets/Knight/knight_slash.png'), 10, 1)

        self.frames = {
            'attack_right' : frames,
            'attack_left' : list(map(lambda surface: pygame.transform.flip(surface, True, False), frames)),

        }
        frames = self.cut_sheet(load_image('Sprite_sheets/Knight/knight_death.png'), 9, 1)
        self.frames['death_right'] = frames
        frames = list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        self.frames['death_left'] = frames
        frames = self.cut_sheet(load_image('Sprite_sheets/Knight/knight_walk.png'), 8, 1)
        self.frames['walk_right'] = frames
        frames = list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        self.frames['walk_left'] = frames
        frames = self.cut_sheet(load_image('Sprite_sheets/Knight/knight_idle.png'), 4, 1)
        self.frames['idle_right'] = frames
        frames = list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        self.frames['idle_left'] = frames
        self.animation = 'walk_left'
        self.cur_frame = 0
        self.image = self.frames[self.animation][self.cur_frame]
        self.rect = self.rect.move(x * tile_width, y * tile_width)


class AnimatedSpriteMH(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        frames = self.cut_sheet(load_image('Sprite_sheets/Main_hero/main_hero.png'), 8, 16)

        self.frames = {
            'idle_right' : frames[0:4],
            'idle_left' : list(map(lambda surface: pygame.transform.flip(surface, True, False), frames[0:4])),
            'walk_right' : frames[9:15],
            'walk_left' : list(map(lambda surface: pygame.transform.flip(surface, True, False), frames[9:15])),
            'attack_right' : frames[35:47],
            'attack_left' : list(map(lambda surface: pygame.transform.flip(surface, True, False), frames[35:47]))
        }
        self.animation = 'walk_right'
        self.cur_frame = 0
        self.onGround = True
        self.xvel = 0
        self.yvel = 0
        self.image = self.frames[self.animation][self.cur_frame]
        self.rect = self.rect.move(x * tile_width, y * tile_width)
    def update2(self, left, right, up, platforms):
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

class AnimatedSpriteWizard(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        frames = self.cut_sheet(load_image('Sprite_sheets/Wizard/wizard_idle.png'), 10, 1)

        self.frames = {
            'idle_right' : frames,
            'idle_left' : list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        }
        frames = self.cut_sheet(load_image('Sprite_sheets/Wizard/wizard_fly_forward.png'), 6, 1)
        self.frames['walk_right'] = frames
        self.frames['walk_left'] = list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        frames = self.cut_sheet(load_image('Sprite_sheets/Wizard/wizard_death.png'), 6, 1)
        self.frames['death_right'] = frames
        self.frames['death_left'] = list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        frames = self.cut_sheet(load_image('Sprite_sheets/Wizard/wizard_slash.png'), 6, 1)
        self.frames['attack_right'] = frames
        self.frames['attack_left'] = list(map(lambda surface: pygame.transform.flip(surface, True, False), frames))
        self.animation = 'walk_left'
        self.cur_frame = 0
        self.image = self.frames[self.animation][self.cur_frame]
        self.rect = self.rect.move(x * tile_width, y * tile_width)