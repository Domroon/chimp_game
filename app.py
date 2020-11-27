import os, sys
import pygame as pg
from pygame.locals import *

if not pg.font:
    print('Warning, fonts disabled')
if not pg.mixer:
    print('Warning, sound disabled')


def load_image(name, colorkey=None):
    # fullname = os.path.join('data', name)
    try:
        image = pg.image.load(name)
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
    # fullname = os.path.join('data', name)
    try:
        sound = pg.mixer.Sound(name)
    except pg.error as message:
        print('Cannot load sound: ', name)
        raise SystemExit(message)
    return sound


class Fist(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('C:/Users/haeus/workspace/chimp_game/data/fist.jpg', -1)
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


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. It can spin the
       monkey when it is punched"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call the Sprite initializer
        self.image, self.rect = load_image('C:/Users/haeus/workspace/chimp_game/data/chimp.jpg', -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
            self.rect = newpos

    def _spin(self):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((936, 240))
    pg.display.set_caption('Monkey Fever')
    pg.mouse.set_visible(0)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pg.display.flip()

    whiff_sound = load_sound('C:/Users/haeus/workspace/chimp_game/data/whiff.wav')
    punch_sound = load_sound('C:/Users/haeus/workspace/chimp_game/data/punch.wav')
    chimp = Chimp()
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((fist, chimp))
    clock = pg.time.Clock()

    while 1:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
