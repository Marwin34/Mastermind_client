import pygame

'''
    Rectangle buttons:
    Note: origin in centre of button.
'''


class Rectangle:
    def __init__(self, x, y, color, text, font, font_size, callback, identity):
        self.x = x
        self.y = y
        self.w = len(text) * 20 + 20
        self.h = font_size + 10
        self.color = pygame.Color(color)

        self.text_len = len(text)

        self.callback = callback
        self.identity = identity
        self.hoovered = False

        self.value = True

        self.active = True

        self.hidden = False

        self.text = pygame.font.Font(font, font_size)
        self.rendered_text = self.text.render(text, 1, (0, 0, 0))

    def draw(self, display):
        if not self.hidden:
            brighter = pygame.Color(100, 100, 100, 0)
            darker = pygame.Color(50, 50, 50, 0)
            if self.hoovered:
                pygame.draw.rect(display, self.color + brighter,
                                 (self.x - self.w / 2, self.y - self.h / 2, self.w, self.h))
            else:
                pygame.draw.rect(display, self.color - darker,
                                 (self.x - self.w / 2, self.y - self.h / 2, self.w, self.h))

            display.blit(self.rendered_text,
                         (self.x - self.w / 2 + 10, self.y - (self.h / 2) + 5))

    def hoover(self, mouse_pos):
        self.hoovered = (self.x - self.w / 2 <= mouse_pos[0] <= self.x - self.w / 2 + self.w and
                         self.y - self.h / 2 <= mouse_pos[1] <= self.y - self.h / 2 + self.h)

    def clicked(self, mouse_buttons_state):
        if mouse_buttons_state[0] and self.hoovered and self.active:
            self.callback(self.identity, self.value)

    def disable(self):
        self.active = False

    def enable(self):
        self.active = True

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False
