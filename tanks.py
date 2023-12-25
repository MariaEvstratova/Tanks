import pygame
import sys
import os

pygame.init()
pygame.mixer.init()
width = 1412
height = 742
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
FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY =(34, 34, 34)
LIGHT_BLUE = (64, 128, 255)
BLUE = (0, 49, 82)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)


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


def start_screen():
    intro_text = ['Игра "Танки"',
                  'Управление:',
                  'Жёлтый танк: для движения кнопки WASD,',
                  ' для стрельбы клавиша F',
                  'Синий танк: для движения стрелки вверх, вниз,',
                  ' вправо, влево, для стрельбы ENTER(RETURN)']

    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    font1 = pygame.font.Font(None, 40)
    text_coord = 120
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
    font2 = pygame.font.Font(None, 40)
    button_coord = text_coord + 50
    size = (200, 60)
    razdel = 50
    l1 = pygame.Surface((size[0], size[1]))
    l2 = pygame.Surface((size[0], size[1]))
    l3 = pygame.Surface((size[0], size[1]))
    l1.fill(WHITE)
    l2.fill(WHITE)
    l3.fill(WHITE)
    screen.blit(l1, ((width / 2) - (size[0] / 2), button_coord))
    screen.blit(l2, ((width / 2) - (size[0] / 2) - razdel - size[0], button_coord))
    screen.blit(l3, ((width / 2) + (size[0] / 2) + razdel, button_coord))

    l1_t1 = font2.render("лёгкий", 1, BLACK)
    l2_t1 = font2.render("средний", 1, BLACK)
    l3_t1 = font2.render("сложный", 1, BLACK)
    l_t2 = font2.render("уровень", 1, BLACK)

    lvl_coord = button_coord + 2 + l1_t1.get_height() + 1
    screen.blit(l_t2, ((width / 2) - (l_t2.get_width() / 2), lvl_coord))
    screen.blit(l_t2, ((width / 2) - (size[0] / 2) - razdel -
                       (size[0] / 2 - l_t2.get_width() / 2) - l_t2.get_width(), lvl_coord))
    screen.blit(l_t2, ((width / 2) + (size[0] / 2) + razdel +
                       (size[0] / 2 - l_t2.get_width() / 2), lvl_coord))

    screen.blit(l2_t1, ((width / 2) - (l2_t1.get_width() / 2), button_coord + 2))
    screen.blit(l1_t1, ((width / 2) - (size[0] / 2) - razdel -
                       (size[0] / 2 - l1_t1.get_width() / 2) - l1_t1.get_width(), button_coord + 2))
    screen.blit(l3_t1, ((width / 2) + (size[0] / 2) + razdel +
                       (size[0] / 2 - l3_t1.get_width() / 2), button_coord + 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] >= ((width / 2) - (size[0] / 2) - razdel - size[0])
                        and event.pos[0] <= ((width / 2) - (size[0] / 2) - razdel)
                        and event.pos[1] >= button_coord and event.pos[1] <= (button_coord + size[1])):
                    level = 'level1.txt'
                    return level
                elif (event.pos[0] >= ((width / 2) - (size[0] / 2))
                      and event.pos[0] <= ((width / 2) - (size[0] / 2) + size[0])
                      and event.pos[1] >= button_coord and event.pos[1] <= (button_coord + size[1])):
                    level = 'level2.txt'
                    return level
                elif (event.pos[0] >= ((width / 2) + (size[0] / 2) + razdel)
                      and event.pos[0] <= ((width / 2) - (size[0] / 2) + size[0])
                      and event.pos[1] >= button_coord and event.pos[1] <= (button_coord + size[1])):
                    level = 'level3.txt'
                    return level
        pygame.display.flip()
        clock.tick(FPS)



class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Bullet:
    def __init__(self, pos_x, pos_y, direct):
        pygame.sprite.Sprite.__init__(self)
        self.direct = direct
        self.image = load_image('bullet.png')
        self.image = pygame.transform.scale(self.image, (10, 5))
        self.image_u = pygame.transform.rotate(self.image, 0)
        self.image_l = pygame.transform.rotate(self.image_u, 90)
        self.image_d = pygame.transform.rotate(self.image_u, 180)
        self.image_r = pygame.transform.rotate(self.image_u, 270)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

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

class TankPink(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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
        self.rect.x = 6
        self.rect.y = 36
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 5
        self.directs = ['left', 'right', 'up', 'down']
        self.direct = 'right'
        self.mask = pygame.mask.from_surface(self.image)
        # (not pygame.sprite.collide_mask(self, horizontal_borders) and
        #  not pygame.sprite.collide_mask(self, vertical_borders))

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

        # if keystate[pygame.K_f]:
        #     bullet = Bullet(self.rect.centerx, self.rect.centerx, self.direct)
        #     if pygame.sprite.spritecollideany(bullet, tank2):
        #         Tank_blue.health -= 1
        #         bullet.kill()
            # for i in barrier_group:
            #     if pygame.sprite.spritecollideany(bullet, i):
            #         i.health -= 1
            #         bullet_group.remove(bullet)
        # if keystate[pygame.K_s] and keystate[pygame.K_d]:
        #     self.image = self.image_dr
        # if keystate[pygame.K_s] and keystate[pygame.K_a]:
        #     self.image = self.image_dl
        # if keystate[pygame.K_w] and keystate[pygame.K_d]:
        #     self.image = self.image_ur
        # if keystate[pygame.K_w] and keystate[pygame.K_a]:
        #     self.image = self.image_ul

        if (pygame.sprite.spritecollideany(self, horizontal_borders) or
                pygame.sprite.spritecollideany(self, vertical_borders) or
                pygame.sprite.collide_mask(self, tank22)):
            self.rect.x = x_old
            self.rect.y = y_old
        for obj in all_sprites:
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
        self.rect.x = width - 5 - 61
        self.rect.y = height - 5 - 61
        self.health = 5
        self.directs = ['left', 'right', 'up', 'down']
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

        if keystate[pygame.K_RETURN]:
            bullet = Bullet(self.rect.centerx, self.rect.centerx, self.direct)
            if pygame.sprite.spritecollideany(bullet, tank2):
                Tank_blue.health -= 1
                bullet_group.remove(bullet)
            # for i in barrier_group:
            #     if pygame.sprite.spritecollideany(bullet, i):
            #         i.health -= 1
            #         bullet_group.remove(bullet)
        # if keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
        #     self.image = self.image_dr
        # if keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]:
        #     self.image = self.image_dl
        # if keystate[pygame.K_UP] and keystate[pygame.K_RIGHT]:
        #     self.image = self.image_ur
        # if keystate[pygame.K_UP] and keystate[pygame.K_LEFT]:
        #     self.image = self.image_ul
        if (pygame.sprite.spritecollideany(self, horizontal_borders) or
                pygame.sprite.spritecollideany(self, vertical_borders) or
                pygame.sprite.collide_mask(self, tank11)):
            self.rect.x = x_old
            self.rect.y = y_old
        for obj in all_sprites:
            if pygame.sprite.collide_mask(self, obj) and obj != self and obj not in aptek_group:
                self.rect.x = x_old
                self.rect.y = y_old


class Apteka(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(aptek_group, all_sprites)
        self.image = load_image('aptek.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect().move(70 * pos_x + 6, 70 * pos_y + 36)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(barrier_group, all_sprites)
        self.image = load_image('kirpich2.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect().move(70 * pos_x + 6, 70 * pos_y + 36)
        self.health = 3
        self.mask = pygame.mask.from_surface(self.image)


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

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    screen.fill((0, 0, 0))
    bullet_group.update()
    tank1.update()
    tank2.update()
    all_sprites.draw(screen)
    tank1.draw(screen)
    tank2.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(100)
terminate()
