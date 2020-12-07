import random
import pygame
import colors


APPLE = pygame.transform.scale(pygame.image.load('images/game/apple.png'), (22, 22))
APPLE = APPLE.convert()
APPLE.set_colorkey((0, 0, 0))
BANANA = pygame.transform.scale(pygame.image.load('images/game/banana.png'), (22, 22))
BANANA = BANANA.convert()
BANANA.set_colorkey((0, 0, 0))
CHERRY = pygame.transform.scale(pygame.image.load('images/game/cherry.png'), (22, 22))
CHERRY = CHERRY.convert()
CHERRY.set_colorkey((0, 0, 0))
KEY = pygame.transform.scale(pygame.image.load('images/game/key.png'), (22, 22))
KEY = KEY.convert()
KEY.set_colorkey((0, 0, 0))
ORANGE = pygame.transform.scale(pygame.image.load('images/game/orange.png'), (22, 22))
ORANGE = ORANGE.convert()
ORANGE.set_colorkey((0, 0, 0))
PEAR = pygame.transform.scale(pygame.image.load('images/game/pear.png'), (22, 22))
PEAR = PEAR.convert()
PEAR.set_colorkey((0, 0, 0))
STRAWBERRY = pygame.transform.scale(pygame.image.load('images/game/strawberry.png'), (22, 22))
STRAWBERRY = STRAWBERRY.convert()
STRAWBERRY.set_colorkey((0, 0, 0))


def text_objects(text, font):
    text_surface = font.render(text, True, colors.WHITE)
    return text_surface, text_surface.get_rect()


# creates a button
def button(screen, msg, x, y, w, h, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (ic[0], ic[1] - 20, ic[2] - 20), (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("default", 30)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


# auxiliary function for drawing text
def text_hollow(text_font, message, font_color):
    not_color = [c ^ 0xFF for c in font_color]
    base = text_font.render(message, 0, font_color, not_color)
    box_size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(box_size, 16)
    img.fill(not_color)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, not_color)
    img.blit(base, (1, 1))
    img.set_colorkey(not_color)
    return img


# auxiliary function for drawing text
def text_outline(text_font, message, font_color, outline_color):
    base = text_font.render(message, 0, font_color)
    outline = text_hollow(text_font, message, outline_color)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img


def apple(item):
    item.weight = random.randint(8, 10)
    item.value = random.randint(3, 5)
    item.item_image = APPLE
    item.name = 'Apple'


def banana(item):
    item.weight = random.randint(6, 8)
    item.value = random.randint(6, 9)
    item.item_image = BANANA
    item.name = 'Banana'


def cherry(item):
    item.weight = random.randint(3, 5)
    item.value = random.randint(8, 10)
    item.item_image = CHERRY
    item.name = 'Cherry'


def key(item):
    item.weight = random.randint(8, 9)
    item.value = random.randint(4, 6)
    item.item_image = KEY
    item.name = 'Key'


def orange(item):
    item.weight = random.randint(5, 7)
    item.value = random.randint(4, 8)
    item.item_image = ORANGE
    item.name = 'Orange'


def pear(item):
    item.weight = random.randint(2, 3)
    item.value = random.randint(2, 4)
    item.item_image = PEAR
    item.name = 'Pear'


def strawberry(item):
    item.weight = random.randint(4, 6)
    item.value = random.randint(6, 8)
    item.item_image = STRAWBERRY
    item.name = 'Strawberry'
