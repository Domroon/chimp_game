import os, sys
import pygame as pg
from pygame.locals import *

if not pg.font:
    print('Warning, fonts disabled')
if not pg.mixer:
    print('Warning, sound disabled')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image: ', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()