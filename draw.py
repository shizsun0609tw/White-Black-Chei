import pygame as pg

class Button(object):
    def __init__(self, position, size, text, button):
        self._pos = position
        self._text = pg.font.SysFont('Comic Sans MS', 30).render(text, False, (0, 0, 0))
        self._type = button
        self._surface = pg.Surface(size)
        self._surface.fill((255, 255, 255))
        self._rect = pg.Rect(position, size)
        self._textRect = pg.Rect((position[0] + 60, position[1]), size)

    def draw(self, screen):
        screen.blit(self._surface, self._rect)
        screen.blit(self._text, self._textRect)
    
    def event_handler(self, event):
        # button click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                return self._type
        if event.type == pg.MOUSEMOTION:
            if self._rect.collidepoint(event.pos):
                self._surface.fill((200, 200, 200))
            else:
                self._surface.fill((255, 255, 255))
        
class Text(object):
    def __init__(self, position, size, text):
        self._pos = position
        self._text = pg.font.SysFont('Comic Sans MS', 30).render(text, False, (0, 0, 0))
        self._rect = pg.Rect(position, size)

    def draw(self, screen):
        screen.blit(self._text, self._rect)
    
    def setText(self, text):
        self._text = pg.font.SysFont('Comic Sans MS', 30).render(text, False, (0, 0, 0))

class Image(object):
    def __init__(self, position, size, path):
        self._pos = position
        self._img = pg.image.load("Assets\\" + path)
        self._rect = pg.Rect(position, size)
        self._img.convert()
        self._visable = False

    def draw(self, screen):
        screen.blit(self._img, self._rect)
        
    def setVisable(self, viable):
        self._visable = viable
        