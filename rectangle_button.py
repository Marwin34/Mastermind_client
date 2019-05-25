import pygame

'''
    Rectangle buttons:
    Note: origin in centre of button.
'''


class Rectangle:
    def __init__(self, x, y, name, callback, identity):
        self.x = x
        self.y = y

        self.callback = callback
        self.identity = identity
        self.hoovered = False

        self.value = True

        self.active = True

        self.hidden = False

        self.sprite_n = pygame.image.load("images/" + name + "_n.png")
        self.sprite_rect_n = self.sprite_n.get_rect()

        self.sprite_h = pygame.image.load("images/" + name + "_h.png")
        self.sprite_rect_h = self.sprite_h.get_rect()

        self.sprite_d = pygame.image.load("images/" + name + "_d.png")
        self.sprite_rect_d = self.sprite_d.get_rect()

        self.w = self.sprite_rect_n.width
        self.h = self.sprite_rect_n.height

    def draw(self, display):
        if not self.hidden:
            if not self.active:
                display.blit(self.sprite_d, (self.x - self.w / 2, self.y - self.h / 2))
            elif self.hoovered:
                display.blit(self.sprite_h, (self.x - self.w / 2, self.y - self.h / 2))
            else:
                display.blit(self.sprite_n, (self.x - self.w / 2, self.y - self.h / 2))

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
