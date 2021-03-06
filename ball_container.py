import numpy as np
import pygame
from pygame import gfxdraw


class Ball:
    def __init__(self, x, y, r, color, callback, identity):
        self.x = x
        self.y = y
        self.r = r
        self.color = pygame.Color(color)
        self.expected_color = color

        self.callback = callback
        self.identity = identity
        self.hoovered = False

        self.active = True

    def draw(self, display):
        brighter = pygame.Color(100, 100, 100, 0)
        darker = pygame.Color(50, 50, 50, 0)
        if self.hoovered and self.active:
            gfxdraw.filled_circle(display, self.x, self.y, self.r, self.color + brighter)
            gfxdraw.aacircle(display, self.x, self.y, self.r, self.color + brighter)
        else:
            gfxdraw.filled_circle(display, self.x, self.y, self.r, self.color - darker)
            gfxdraw.aacircle(display, self.x, self.y, self.r, self.color - darker)

    def hoover(self, mouse_pos):
        self.hoovered = np.sqrt((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) <= self.r

    def expect_color(self, color):
        self.expected_color = color

    def clicked(self, mouse_buttons_state):
        if mouse_buttons_state[0] and self.hoovered and self.active:
            self.color = pygame.Color(self.expected_color)
            self.callback(self.identity, self.expected_color)

    def set_color(self, color):
        self.color = pygame.Color(color)

    def disable(self):
        self.active = False

    def enable(self):
        self.active = True

    def reset_value(self):
        self.expected_color = 'gray'
        self.color = pygame.Color(self.expected_color)
