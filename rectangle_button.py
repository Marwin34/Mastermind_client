import pygame


class Rectangle:
    def __init__(self, x, y, w, h, color, text, font, font_size, callback, identity):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = pygame.Color(color)

        self.callback = callback
        self.identity = identity
        self.hoovered = False

        self.value = True

        self.text = pygame.font.Font(font, font_size)
        self.rendered_text = self.text.render(text, 1, (0, 0, 0))

    def draw(self, display):
        brighter = pygame.Color(100, 100, 100, 0)
        darker = pygame.Color(50, 50, 50, 0)
        if self.hoovered:
            pygame.draw.rect(display, self.color + brighter, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.color - darker, (self.x, self.y, self.w, self.h))

        display.blit(self.rendered_text, (self.x + self.w / 2 - (18 * 4) / 2, self.y + (self.h / 2) - (36 / 2)))

    def hoover(self, mouse_pos):
        self.hoovered = (self.x <= mouse_pos[0] <= self.x + self.w and
                         self.y <= mouse_pos[1] <= self.y + self.h)

    def clicked(self, mouse_buttons_state):
        if mouse_buttons_state[0] and self.hoovered:
            self.callback(self.identity, self.value)