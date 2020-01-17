import pygame, sys, os
from Animated_sprites import AnimatedSpriteDemon, AnimatedSpriteKnight, AnimatedSpriteMH, AnimatedSpriteWizard, all_sprites, MOVE_SPEED, JUMP_POWER, GRAVITY, mob_group, player_group
from shield_bars import draw_shield_bar_demon, draw_shield_bar_mobs


COLUMS = 33
ROWS = 256
tile_width = tile_height = 64

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
size = width, height = screen.get_rect()[2:]

clock = pygame.time.Clock()
FPS = 60
BACKGROUNDCOLOR = pygame.Color(64, 32, 0)
TEXTCOLOR = pygame.Color(218, 189, 171)
SHADOWTEXT = pygame.Color(218, 189, 171)
hsv = SHADOWTEXT.hsva
SHADOWTEXT.hsva = (hsv[0], hsv[1], hsv[2] - 50, hsv[3])
FONT = 'agencyfb'

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

GREEN = pygame.Color('green')
WHITE = pygame.Color('white')

left = False
up = False
right = False
die = False
platforms = []
platforms_2 = []
mobs = []

tiles_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Can't load image:", name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

#=======================================================================================================================
tile_images = {'wall': pygame.transform.scale(load_image('box.png'), (64, 64)), 'empty': pygame.transform.scale(load_image('grass.png'), (64, 64)),
               'grass1': pygame.transform.scale(load_image('grass1.png'), (64, 64))}

#=======================================================================================================================


class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 0
        self.top = 0
        self.cell_size = cell_size

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

#=======================================================================================================================


#=======================================================================================================================



#=======================================================================================================================

#=======================================================================================================================

#=======================================================================================================================


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):#, sheet, columns, rows, x, y):
        super().__init__(all_sprites, tiles_group)
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

def terminate():
    pygame.quit()
    sys.exit()
#=======================================================================================================================

def main_screen():  # todo класс заставки
    introtext = ['Чтобы начать игру, '
                 'Нажмите любую кнопку']
    nametext = ['Dungeon story']
    blackname = ['Dungeon story']

    background = pygame.transform.scale(load_image('fon.jpg'), (1920, 1080))
    screen.blit(background, (0, 0))
    intro_font = pygame.font.Font(None, 50)
    name_font = pygame.font.SysFont(FONT, 150)
    black_font = pygame.font.SysFont(FONT, 160)
    text_coord = 1000
    name_coord = 50
    black_coord = 50

    black_rendered = black_font.render(blackname[0], 1, SHADOWTEXT)
    black_rect = black_rendered.get_rect()
    black_coord += 10
    black_rect.top = black_coord
    black_rect.x = (1920 - black_rect.width) // 2
    black_coord += black_rect.height
    screen.blit(black_rendered, black_rect)

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
#=======================================================================================================================
def game_over():
    background = pygame.transform.scale(load_image('game_over.jpg'), (1920, 1080))
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                terminate()

        pygame.display.flip()
#=======================================================================================================================
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, all_sprites, tiles_group, player_group):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ' ':
                Tile('empty', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                tile = Tile('wall', x, y)
                platforms.append(tile)
            elif level[y][x] == '/':
                tile_2 = Tile('wall', x, y)
                platforms_2.append(tile_2)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = AnimatedSpriteMH(x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                new_demon = AnimatedSpriteDemon(x, y)
                mobs.append(new_demon)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                new_knight = AnimatedSpriteKnight(x, y)
                mobs.append(new_knight)
            elif level[y][x] == '*':
                Tile('grass1', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                new_wizard = AnimatedSpriteWizard(x, y)
                mobs.append(new_wizard)

    return new_wizard, new_knight, new_demon, new_player, x, y

#=======================================================================================================================
def game_menu():
    exit_text = ['Выход']
    continue_text = ['Продолжить']

    background = pygame.transform.scale(load_image('menu.png'), (1920, 1080))
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

#=======================================================================================================================
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 30
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
#=======================================================================================================================
running = True
camera = Camera()
cell_size = 80

#=======================================================================================================================
main_screen()
wizard, knight, demon, player, level_x, level_y = generate_level(load_level('level.txt'), all_sprites, tiles_group, player_group)
player.rect.width = 60
player.rect.height = 60
demon.rect.w = demon.rect.h = 256
wizard.rect.x -= 200
knight.rect.x -= 200
demon.rect.x -= 200

while running:
    rasst_dem = player.rect.center[0] - demon.rect.center[0]
    rasst = player.rect.center[0] - wizard.rect.center[0]
    rasst_move = player.rect.x - wizard.rect.x
    rasst_kn = player.rect.center[0] - knight.rect.center[0]
    rasst_kn_move = player.rect.x - knight.rect.x
    for m in mobs:
        if pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_mask):
            player.shield -= 1

    for p in platforms:
        if pygame.sprite.collide_rect(knight, p):
            pass

    if player.shield <= 0:
        running = False
    if wizard.shield <= 0:
        wizard.kill()
    if knight.shield <= 0:
        knight.kill()
    if demon.shield < 0:
        demon.kill()
        demon.shield = 0

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
                die = True

            # реализация атаки Главного Героя
            if event.key == pygame.K_l:
                if -128 < rasst_dem < 128:
                    demon.shield -= 5

                elif -128 < rasst < 128:
                    wizard.shield -= 5

                elif -128 < rasst_kn < 128:
                    knight.shield -= 5

    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    pressed = pygame.key.get_pressed()
    up = pressed[pygame.K_w]
    right = pressed[pygame.K_d]
    left = pressed[pygame.K_a]

    if die:
        game_over()
    screen.fill(BACKGROUNDCOLOR)
    player.update2(left, right, up, platforms)

    if rasst_dem > 128:
        demon.move_left()
    elif rasst_dem < -128:
        demon.move_right()
    else:
        if rasst_dem >= 0:
            demon.attack_right()
        else:
            demon.attack_left()

    if rasst_move > 128:
        wizard.rect.x += 2
        wizard.move_left()
    elif rasst_move < -128:
        wizard.rect.x -= 2
        wizard.move_right()
    else:
        if rasst_move > 0:
            wizard.attack_right()
        else:
            wizard.attack_left()

    if rasst_kn_move > 128:
        knight.rect.x += 2
        knight.move_right()
    elif rasst_kn_move < -128:
        knight.rect.x -= 2
        knight.move_left()
    else:
        if rasst_kn_move > 0:
            knight.attack_right()
        else:
            knight.attack_left()

    player.update()
    demon.update1()
    knight.update()
    wizard.update()

    tiles_group.draw(screen)
    mob_group.draw(screen)
    player_group.draw(screen)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_shield_bar_demon(screen, demon.rect.x, demon.rect.y, demon.shield)
    draw_shield_bar_mobs(screen, knight.rect.x, knight.rect.y, knight.shield)
    draw_shield_bar_mobs(screen, wizard.rect.x, wizard.rect.y, wizard.shield)
    pygame.display.flip()

pygame.quit()
