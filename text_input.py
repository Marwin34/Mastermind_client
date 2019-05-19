import pygame


class TextInput:
    def __init__(self, x, y, w, h, font, font_size, callback, identity):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.callback = callback
        self.identity = identity

        self.color = pygame.Color('white')

        self.value = ""
        self.visible_part = ""

        self.text = pygame.font.Font(font, font_size)
        self.rendered_text = self.text.render(self.value, 1, (0, 0, 0))

        self.focused = False

        self.hoovered = False

    def draw(self, display):
        brighter = pygame.Color(100, 100, 100, 0)
        darker = pygame.Color(50, 50, 50, 0)
        if self.hoovered or self.focused:
            pygame.draw.rect(display, self.color + brighter, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.color - darker, (self.x, self.y, self.w, self.h))

        self.rendered_text = self.text.render(self.visible_part, 1, (0, 0, 0))
        display.blit(self.rendered_text, (self.x, self.y + (self.h / 2) - (36 / 2)))

    def hoover(self, mouse_pos):
        self.hoovered = (self.x <= mouse_pos[0] <= self.x + self.w and
                         self.y <= mouse_pos[1] <= self.y + self.h)

    def clicked(self, mouse_buttons_state):
        if mouse_buttons_state[0] and self.hoovered:
            self.focused = True
        elif mouse_buttons_state[0] and not self.hoovered:
            self.focused = False

    def key_pressed(self, key):
        key_code = key[0]
        key_unicode = key[1]

        if self.focused:
            if (48 <= key_code <= 57) or (65 <= key_code <= 90) or (97 <= key_code <= 122):
                self.value += key_unicode
            elif key_code == 8:
                self.value = self.value[0:-1]

            if len(self.value) * 20 > self.w:
                self.visible_part = self.value[-len(self.visible_part):]
            else:
                self.visible_part = self.value

            self.callback(self.identity, self.value)
