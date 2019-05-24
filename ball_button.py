import numpy as np
import pygame
from pygame import gfxdraw


class Ball:
    def __init__(self, x, y, r, color, callback, identity):
        self.x = x
        self.y = y
        self.r = r
        self.color = pygame.Color(color)

        self.callback = callback
        self.identity = identity
        self.hoovered = False

        self.value = True

    def draw(self, display):
        brighter = pygame.Color(100, 100, 100, 0)
        darker = pygame.Color(50, 50, 50, 0)
        if self.hoovered:
            gfxdraw.filled_circle(display, self.x, self.y, self.r, self.color + brighter)
            gfxdraw.aacircle(display, self.x, self.y, self.r, self.color + brighter)
        else:
            gfxdraw.filled_circle(display, self.x, self.y, self.r, self.color - darker)
            gfxdraw.aacircle(display, self.x, self.y, self.r, self.color - darker)

    def hoover(self, mouse_pos):
        self.hoovered = np.sqrt((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) <= self.r

    def clicked(self, mouse_buttons_state):
        if mouse_buttons_state[0] and self.hoovered:
            self.callback(self.identity, self.value)
