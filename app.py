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


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error as message:
        print('Cannot load sound: ', fullname)
        raise SystemExit(message)
    return sound


class Fist(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('fist.jpg', -1)
        self.punching = 0

    def update(self):
        """move the fist based on the mouse position"""
        pos = pg.mouse.get_pos()
        self.rect.midtop = pos

    def punch(self, target):
        """returns true if the fist collide with the target"""
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """called to pull the fist back"""
        self.punching = 0
