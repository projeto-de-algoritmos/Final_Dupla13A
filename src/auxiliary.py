import random
import pygame


APPLE = pygame.transform.scale(pygame.image.load('../images/game/apple.png'), (22, 22))
APPLE = APPLE.convert()
APPLE.set_colorkey((0, 0, 0))
BANANA = pygame.transform.scale(pygame.image.load('../images/game/banana.png'), (22, 22))
BANANA = BANANA.convert()
BANANA.set_colorkey((0, 0, 0))
CHERRY = pygame.transform.scale(pygame.image.load('../images/game/cherry.png'), (22, 22))
CHERRY = CHERRY.convert()
CHERRY.set_colorkey((0, 0, 0))
KEY = pygame.transform.scale(pygame.image.load('../images/game/key.png'), (22, 22))
KEY = KEY.convert()
KEY.set_colorkey((0, 0, 0))
ORANGE = pygame.transform.scale(pygame.image.load('../images/game/orange.png'), (22, 22))
ORANGE = ORANGE.convert()
ORANGE.set_colorkey((0, 0, 0))
PEAR = pygame.transform.scale(pygame.image.load('../images/game/pear.png'), (22, 22))
PEAR = PEAR.convert()
PEAR.set_colorkey((0, 0, 0))
STRAWBERRY = pygame.transform.scale(pygame.image.load('../images/game/strawberry.png'), (22, 22))
STRAWBERRY = STRAWBERRY.convert()
STRAWBERRY.set_colorkey((0, 0, 0))


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
