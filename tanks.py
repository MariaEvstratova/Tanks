import pygame
import sys
import os


pygame.init()
pygame.mixer.init()
width = 1412
height = 742
delay1 = 0
delay2 = 0
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Танчики")
clock = pygame.time.Clock()
barrier_group = pygame.sprite.Group()
aptek_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
tank1 = pygame.sprite.Group()
tank2 = pygame.sprite.Group()
blue_hearts = pygame.sprite.Group()
pink_hearts = pygame.sprite.Group()
group_of_sprites = [tank1, tank2, vertical_borders, horizontal_borders,
                    bullet_group, aptek_group, barrier_group]

font = pygame.font.Font(None, 60)
FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (34, 34, 34)
GRAY1 = (80, 80, 80)
LIGHT_BLUE = (64, 128, 255)
BLUE = (116, 146, 255)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
ORANGE = (245, 138, 39)

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Barrier(x, y)
            elif level[y][x] == 'H':
                Apteka(x, y)

def draw():
    intro_text = ['Игра "ТАНКИ"']
    fon = pygame.transform.scale(load_image('fon 5.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    # screen.fill(BLUE)
    font = pygame.font.Font('TunnelFront/TunnelFront.ttf', 100)
    font1 = pygame.font.Font('TunnelFront/TunnelFront.ttf', 40)
    text_coord = 80
    for line in intro_text:
        if line == intro_text[0]:
            string_rendered = font.render(line, 1, BLACK)
        else:
            string_rendered = font1.render(line, 1, GRAY)
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = (width / 2) - (string_rendered.get_width() / 2)
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    button_coord = text_coord + 80
    size = (300, 80)
    razdel = 20
    l1 = load_image("button.png")
    l2 = load_image("button.png")
    l3 = load_image("button.png")
    l4 = load_image("button.png")
    t1 = pygame.transform.scale(load_image('tank_pink.png'), (200, 200))
    t2 = pygame.transform.scale(load_image('tank_blue.png'), (200, 200))
    screen.blit(l1, ((width / 2) - (size[0] / 2), button_coord))
    screen.blit(l2, ((width / 2) - (size[0] / 2), button_coord + size[1] + razdel))
    screen.blit(l3, ((width / 2) - (size[0] / 2), button_coord + size[1] * 2 + razdel * 2))
    screen.blit(l4, ((width / 2) - (size[0] / 2), button_coord + size[1] * 3 + razdel * 3))

    l1_t1 = font1.render("лёгкий", 1, GRAY)
    l2_t1 = font1.render("средний", 1, GRAY)
    l3_t1 = font1.render("сложный", 1, GRAY)
    l_t2 = font1.render("уровень", 1, GRAY)
    l4 = font1.render("управление", 1, GRAY)

    razdel1 = 15
    lvl_coord = button_coord + l1_t1.get_height()
    screen.blit(l_t2, ((width / 2) - (l_t2.get_width() / 2), lvl_coord - 7))
    screen.blit(l_t2, ((width / 2) - (l_t2.get_width() / 2), lvl_coord + size[1] + razdel1 - 5))
    screen.blit(l_t2, ((width / 2) - (l_t2.get_width() / 2), lvl_coord + size[1] * 2 + razdel1 * 2))

    screen.blit(l1_t1, ((width / 2) - (l1_t1.get_width() / 2), button_coord + 5))
    screen.blit(l2_t1, ((width / 2) - (l2_t1.get_width() / 2), button_coord + size[1] + razdel + 5))
    screen.blit(l3_t1, ((width / 2) - (l3_t1.get_width() / 2), button_coord + size[1] * 2 + razdel * 2 + 5))

    screen.blit(l4, ((width / 2) - (l4.get_width() / 2), button_coord + size[1] * 3 + razdel * 3 + 15))

    return [size, button_coord, razdel]


def start_screen():
    size, button_coord, razdel = draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] >= ((width / 2) - (size[0] / 2))
                      and event.pos[0] <= ((width / 2) - (size[0] / 2) + size[0])
                      and event.pos[1] >= button_coord and event.pos[1] <= (button_coord + size[1])):
                    level = 'level1.txt'
                    return level
                elif (event.pos[0] >= ((width / 2) - (size[0] / 2))
                      and event.pos[0] <= ((width / 2) - (size[0] / 2) + size[0])
                      and event.pos[1] >= button_coord + size[1] + razdel
                      and event.pos[1] <= (button_coord + size[1] + razdel + size[1])):
                    level = 'level2.txt'
                    return level
                elif (event.pos[0] >= ((width / 2) - (size[0] / 2))
                      and event.pos[0] <= ((width / 2) - (size[0] / 2) + size[0])
                      and event.pos[1] >= button_coord + size[1] * 2 + razdel * 2
                      and event.pos[1] <= (button_coord + size[1] * 2 + razdel * 2 + size[1])):
                    level = 'level3.txt'
                    return level
                elif (event.pos[0] >= ((width / 2) - (size[0] / 2))
                      and event.pos[0] <= ((width / 2) - (size[0] / 2) + size[0])
                      and event.pos[1] >= button_coord + size[1] * 3 + razdel * 3
                      and event.pos[1] <= (button_coord + size[1] * 3 + razdel * 3 + size[1])):
                    upravl()
        size, button_coord, razdel = draw()
        pygame.display.flip()
        clock.tick(FPS)


def upravl():
    fon = load_image('Upravlenie.png')
    screen.blit(fon, (width / 2 - fon.get_width() / 2 + 20, height / 2 - fon.get_height() / 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 1045 and event.pos[0] <= 1070 and (event.pos[1] >= 70 and event.pos[1] <= 100):
                    return

        pygame.display.flip()
        clock.tick(FPS)


def end_screen(winner, loser):
    screen.fill((0, 0, 0))
    fon = load_image('game_over.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('TunnelFront/TunnelFront.ttf', 90)
    text_winner = font.render(winner, True, WHITE)
    screen.blit(text_winner, (68 + 274 + 10, 378))
    text_winner = font.render(loser, True, WHITE)
    screen.blit(text_winner, (760 + 229 + 10, 378))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 273 and event.pos[0] <= 273 + 407 and (event.pos[1] >= 564 and event.pos[1] <= 564 + 109):
                    for i in group_of_sprites:
                        for j in i:
                            j.kill()
                    level = start_screen()
                    Border(5, 35, width - 5, 35)
                    Border(5, height - 5, width - 5, height - 5)
                    Border(5, 35, 5, height - 5)
                    Border(width - 5, 35, width - 5, height - 5)
                    tank11 = TankPink()
                    tank1.add(tank11)
                    tank22 = TankBlue()
                    tank2.add(tank22)
                    generate_level(load_level(level))
                    PinkHeart(25, 0)
                    BlueHeart(width - 35, 0)
                    return tank11, tank22
                elif event.pos[0] >= 727 and event.pos[0] <= 727 + 407 and (event.pos[1] >= 564 and event.pos[1] <= 564 + 109):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill((0, 0, 0))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill((0, 0, 0))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, direct, other):
        super().__init__(all_sprites, bullet_group)
        self.direct = direct
        self.width = width
        self.height = height
        self.other = other
        self.image = pygame.transform.rotate(load_image('bullet.png'), 90)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image_u = pygame.transform.rotate(self.image, 0)
        self.image_l = pygame.transform.rotate(self.image_u, 90)
        self.image_d = pygame.transform.rotate(self.image_u, 180)
        self.image_r = pygame.transform.rotate(self.image_u, 270)
        self.image_dr = pygame.transform.rotate(self.image_u, 225)
        self.image_dl = pygame.transform.rotate(self.image_u, 135)
        self.image_ur = pygame.transform.rotate(self.image_u, 305)
        self.image_ul = pygame.transform.rotate(self.image_u, 45)
        if self.direct == 'left':
            self.rect = self.image.get_rect().move(pos_x - 1, pos_y + self.height / 2)
        elif self.direct == 'right':
            self.rect = self.image.get_rect().move(pos_x + self.width + 1, pos_y + self.height / 2)
        elif self.direct == 'up':
            self.rect = self.image.get_rect().move(pos_x + self.width / 2, pos_y + 1)
        elif self.direct == 'down':
            self.rect = self.image.get_rect().move(pos_x + self.width / 2, pos_y + self.height + 1)
        elif self.direct == 'r_down':
            self.rect = self.image.get_rect().move(pos_x + self.width + 1, pos_y + self.height + 1)
        elif self.direct == 'l_down':
            self.rect = self.image.get_rect().move(pos_x + 1, pos_y + self.height + 1)
        elif self.direct == 'r_up':
            self.rect = self.image.get_rect().move(pos_x + self.width + 1, pos_y + 1)
        elif self.direct == 'l_up':
            self.rect = self.image.get_rect().move(pos_x + 1, pos_y + 1)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.direct == 'left':
            self.image = self.image_l
            self.rect.x -= 1
        if self.direct == 'right':
            self.image = self.image_r
            self.rect.x += 1
        if self.direct == 'up':
            self.image = self.image_u
            self.rect.y -= 1
        if self.direct == 'down':
            self.image = self.image_d
            self.rect.y += 1
        if self.direct == 'r_down':
            self.image = self.image_dr
            self.rect.x += 1
            self.rect.y += 1
        if self.direct == 'l_down':
            self.image = self.image_dl
            self.rect.x -= 1
            self.rect.y += 1
        if self.direct == 'r_up':
            self.image = self.image_ur
            self.rect.x += 1
            self.rect.y -= 1
        if self.direct == 'l_up':
            self.image = self.image_ul
            self.rect.x -= 1
            self.rect.y -= 1

        for group in group_of_sprites:
            if group != bullet_group and group != self.other and group != aptek_group:
                if group == barrier_group:
                    for obj in barrier_group:
                        if pygame.sprite.collide_mask(self, obj):
                            obj.health -= 1
                            self.kill()
                            break
                elif pygame.sprite.spritecollideany(self, group) and group == tank1:
                    tank11.health_pink -= 1
                    self.kill()
                elif pygame.sprite.spritecollideany(self, group) and group == tank2:
                    tank22.health_blue -= 1
                    self.kill()
                elif pygame.sprite.spritecollideany(self, group):
                    self.kill()

class TankPink(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("tank_pink.png")
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.image_u = pygame.transform.rotate(self.image, 0)
        self.image_l = pygame.transform.rotate(self.image_u, 90)
        self.image_d = pygame.transform.rotate(self.image_u, 180)
        self.image_r = pygame.transform.rotate(self.image_u, 270)
        self.image_dr = pygame.transform.rotate(self.image_u, 225)
        self.image_dl = pygame.transform.rotate(self.image_u, 135)
        self.image_ur = pygame.transform.rotate(self.image_u, 305)
        self.image_ul = pygame.transform.rotate(self.image_u, 45)
        self.image = self.image_r
        self.rect = self.image.get_rect()
        self.rect.x = 8
        self.rect.y = 38
        self.mask = pygame.mask.from_surface(self.image)
        self.health_pink = 5
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery
        self.directs = ['left', 'right', 'up', 'down', 'r_down', 'l_down', 'r_up', 'l_up']
        self.direct = 'right'
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        x_old, y_old = self.rect.x, self.rect.y
        keystate = pygame.key.get_pressed()
        self.x = 0
        if keystate[pygame.K_a]:
            self.direct = self.directs[0]
            self.x = -1
            self.image = self.image_l
            self.rect.x += self.x
        if keystate[pygame.K_d]:
            self.direct = self.directs[1]
            self.x = 1
            self.image = self.image_r
            self.rect.x += self.x

        if keystate[pygame.K_s]:
            self.direct = self.directs[3]
            self.y = 1
            self.rect.y += self.y
            self.image = self.image_d
        if keystate[pygame.K_w]:
            self.direct = self.directs[2]
            self.y = -1
            self.rect.y += self.y
            self.image = self.image_u

        if keystate[pygame.K_s] and keystate[pygame.K_d]:
            self.image = self.image_dr
            self.direct = self.directs[4]
        if keystate[pygame.K_s] and keystate[pygame.K_a]:
            self.image = self.image_dl
            self.direct = self.directs[5]
        if keystate[pygame.K_w] and keystate[pygame.K_d]:
            self.image = self.image_ur
            self.direct = self.directs[6]
        if keystate[pygame.K_w] and keystate[pygame.K_a]:
            self.image = self.image_ul
            self.direct = self.directs[7]

        if (pygame.sprite.spritecollideany(self, horizontal_borders) or
                pygame.sprite.spritecollideany(self, vertical_borders) or
                pygame.sprite.collide_mask(self, tank22)):
            self.rect.x = x_old
            self.rect.y = y_old

        for obj in all_sprites:
            if obj in aptek_group and pygame.sprite.collide_mask(self, obj):
                obj.kill()
                self.health_pink += 1
            if pygame.sprite.collide_mask(self, obj) and obj != self and obj not in aptek_group:
                self.rect.x = x_old
                self.rect.y = y_old


class TankBlue(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("tank_blue.png")
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.image_u = pygame.transform.rotate(self.image, 0)
        self.image_l = pygame.transform.rotate(self.image_u, 90)
        self.image_d = pygame.transform.rotate(self.image_u, 180)
        self.image_r = pygame.transform.rotate(self.image_u, 270)
        self.image_dr = pygame.transform.rotate(self.image_u, 225)
        self.image_dl = pygame.transform.rotate(self.image_u, 135)
        self.image_ur = pygame.transform.rotate(self.image_u, 305)
        self.image_ul = pygame.transform.rotate(self.image_u, 45)
        self.image = self.image_l
        self.rect = self.image.get_rect()
        self.center_x = self.rect.x + self.rect.width / 2
        self.center_y = self.rect.y + self.rect.height / 2
        self.rect.x = width - 5 - 61
        self.rect.y = height - 5 - 61
        self.health_blue = 5
        self.directs = ['left', 'right', 'up', 'down', 'r_down', 'l_down', 'r_up', 'l_up']
        self.direct = 'left'
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        x_old, y_old = self.rect.x, self.rect.y
        keystate = pygame.key.get_pressed()
        self.x = 0
        if keystate[pygame.K_LEFT]:
            self.direct = self.directs[0]
            self.x = -1
            self.image = self.image_l
            self.rect.x += self.x
        if keystate[pygame.K_RIGHT]:
            self.direct = self.directs[1]
            self.x = 1
            self.image = self.image_r
            self.rect.x += self.x
        if keystate[pygame.K_DOWN]:
            self.direct = self.directs[3]
            self.y = 1
            self.rect.y += self.y
            self.image = self.image_d
        if keystate[pygame.K_UP]:
            self.direct = self.directs[2]
            self.y = -1
            self.rect.y += self.y
            self.image = self.image_u

        if keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
            self.image = self.image_dr
            self.direct = self.directs[4]
        if keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]:
            self.image = self.image_dl
            self.direct = self.directs[5]
        if keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]:
            self.image = self.image_ur
            self.direct = self.directs[6]
        if keystate[pygame.K_UP] and keystate[pygame.K_LEFT]:
            self.image = self.image_ul
            self.direct = self.directs[7]

        if (pygame.sprite.spritecollideany(self, horizontal_borders) or
                pygame.sprite.spritecollideany(self, vertical_borders) or
                pygame.sprite.collide_mask(self, tank11)):
            self.rect.x = x_old
            self.rect.y = y_old

        for obj in all_sprites:
            if obj in aptek_group and pygame.sprite.collide_mask(self, obj):
                self.health_blue += 1
                obj.kill()
            if pygame.sprite.collide_mask(self, obj) and obj != self and obj not in aptek_group:
                self.rect.x = x_old
                self.rect.y = y_old



class Apteka(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(aptek_group, all_sprites)
        self.image = load_image('aptek.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(70 * pos_x + 16, 70 * pos_y + 46)
        self.mask = pygame.mask.from_surface(self.image)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(barrier_group, all_sprites)
        self.image = load_image('kaktus.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect().move(70 * pos_x + 6, 70 * pos_y + 36)
        self.health = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.health == 1:
            broken = load_image('broken_kaktus3.png')
            broken = pygame.transform.scale(broken, (70, 70))
            self.image = broken
        if self.health <= 0:
            self.kill()


class PinkHeart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(pink_hearts, all_sprites)
        self.image = load_image('pink_heart.png')
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class BlueHeart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blue_hearts, all_sprites)
        self.image = load_image('blue_heart.png')
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect().move(pos_x, pos_y)


level = start_screen()
Border(5, 35, width - 5, 35)
Border(5, height - 5, width - 5, height - 5)
Border(5, 35, 5, height - 5)
Border(width - 5, 35, width - 5, height - 5)
tank11 = TankPink()
tank1.add(tank11)
tank22 = TankBlue()
tank2.add(tank22)
generate_level(load_level(level))
PinkHeart(25, 0)
BlueHeart(width - 35, 0)
fon = pygame.transform.scale(load_image('orange.jpeg'), (width - 10, height - 35 - 5))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if delay1 == 0:
                    bullet = Bullet(tank22.rect.x, tank22.rect.y, tank22.rect.width, tank22.rect.height, tank22.direct, tank2)
                    delay1 = 60
            if event.key == pygame.K_f:
                if delay2 == 0:
                    bullet = Bullet(tank11.rect.x, tank11.rect.y, tank11.rect.width, tank11.rect.height, tank11.direct, tank1)
                    delay2 = 60
    screen.fill((255, 255, 255))
    screen.blit(fon, (5, 35))
    tank1.update()
    tank2.update()
    bullet_group.update()
    all_sprites.draw(screen)
    bullet_group.draw(screen)
    tank1.draw(screen)
    tank2.draw(screen)
    text_pink_hearts = font.render(str(tank11.health_pink), True, BLACK)
    screen.blit(text_pink_hearts, [0, 0])
    text_blue_hearts = font.render(str(tank22.health_blue), True, BLACK)
    screen.blit(text_blue_hearts, [width - 25 - 35, 0])
    if tank11.health_pink == 0:
        tank11, tank22 = end_screen('синий', 'розовый')
    elif tank22.health_blue == 0:
        tank11, tank22 = end_screen('розовый', 'синий')
    all_sprites.update()
    if delay1 != 0:
        delay1 -= 1
    if delay2 != 0:
        delay2 -= 1
    pygame.display.flip()
    clock.tick(100)
terminate()
