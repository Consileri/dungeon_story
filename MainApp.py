import pygame

from Camera import Camera
from utils import load_image, terminate, load_level
from Animated_sprites import AnimatedSpriteDemon, AnimatedSpriteKnight, AnimatedSpriteMH, AnimatedSpriteWizard, \
    all_sprites, mob_group, player_group
from shield_bars import draw_shield_bar_demon, draw_shield_bar_mobs, draw_shield_bar


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

left = False
up = False
right = False
die = False
platforms = []
platforms_2 = []
mobs = []

tiles_group = pygame.sprite.Group()

tile_images = {'wall': pygame.transform.scale(load_image('box.png'), (64, 64)),
               'empty': pygame.transform.scale(load_image('grass.png'), (64, 64)),
               'grass1': pygame.transform.scale(load_image('grass1.png'), (64, 64))}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


def main_screen():
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


def generate_level(level, all_sprites, tiles_group, player_group):
    new_player, x, y = None, None, None
    wz_list, kn_list = [], []
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
                kn_list.append(new_knight)
                mobs.append(new_knight)
            elif level[y][x] == '*':
                Tile('grass1', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                new_wizard = AnimatedSpriteWizard(x, y)
                wz_list.append(new_wizard)
                mobs.append(new_wizard)

    return wz_list, kn_list, new_demon, new_player, x, y


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
                if (exit_rect.x < pos[0] < (exit_rect.width + exit_rect.x)) and \
                        (exit_rect.y < pos[1] < (exit_rect.height + exit_rect.y)):
                    terminate()
                elif (continue_rect.x < pos[0] < (continue_rect.width + continue_rect.x)) and \
                        (continue_rect.y < pos[1] < (continue_rect.height + continue_rect.y)):
                    return
        pygame.display.flip()
        clock.tick(FPS)


running = True
camera = Camera()
cell_size = 80

main_screen()

wz_list, kn_list, demon, player, level_x, level_y = generate_level(load_level('level.txt'),
                                                                 all_sprites, tiles_group, player_group)
player.rect.width = 60
player.rect.height = 60
demon.rect.w = demon.rect.h = 256

while running:
    rasst_dem = player.rect.center[0] - demon.rect.center[0]

    for m in mobs:
        if m.shield <= 0:
            m.kill()
            mobs.remove(m)

    for m in mobs:
        if pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_mask):
            player.shield -= 0.2

    if player.shield <= 0:
        die = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Выход при нажатии Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_menu()

            # реализация атаки Главного Героя
            if event.key == pygame.K_l:
                if -128 < rasst_dem < 128:
                    player.attack_left()
                    demon.shield -= 5

                for wz in wz_list:
                    if -800 > player.rect.center[0] - wz.rect.center[0] > -900:
                        wz.shield -= 5
                for kn in kn_list:
                    if -128 < player.rect.center[0] - kn.rect.center[0] < 128:
                        kn.shield -= 5

    camera.update(player)

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

    for wz in wz_list:
        wz.update2()
    for kn in kn_list:
        kn.update2()

    if rasst_dem > 128:
        demon.move_right()
    elif rasst_dem < -128:
        demon.move_left()
    else:
        if rasst_dem >= 0:
            demon.attack_right()
        else:
            demon.attack_left()

    for wz in wz_list:
        if -128 < player.rect.x - wz.rect.x < 0:
            wz.attack_right()
        elif 0 < player.rect.x - wz.rect.x < 128:
            wz.attack_left()

    for kn in kn_list:
        if -128 < player.rect.x - kn.rect.x < 0:
            kn.attack_left()
        elif 0 < player.rect.x - kn.rect.x < 128:
            kn.attack_right()

    player.update()
    demon.update1()

    tiles_group.draw(screen)
    mob_group.draw(screen)
    mob_group.update()
    player_group.draw(screen)

    draw_shield_bar(screen, 5, 5, player.shield)

    if demon.shield > 0:
        draw_shield_bar_demon(screen, demon.rect.x, demon.rect.y, demon.shield)
    for kn in kn_list:
        if kn.shield > 0:
            draw_shield_bar_mobs(screen, kn.rect.x, kn.rect.y, kn.shield)
    for wz in wz_list:
        if wz.shield > 0:
            draw_shield_bar_mobs(screen, wz.rect.x, wz.rect.y, wz.shield)

    pygame.display.flip()

pygame.quit()
