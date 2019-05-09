import numpy as np
import pygame
import ball_button
import ball_container


class GUI:
    def __init__(self, display):
        self.display = display

        self.input = {
            'send': False,
            'mouse_pos': (0, 0),
            'LPM': 0,
            'color_picker_red': False,
            'color_picker_blue': False,
            'color_picker_green': False,
            'color_picker_yellow': False,
            'color_slot_1': 'gray',
            'color_slot_2': 'gray',
            'color_slot_3': 'gray',
            'color_slot_4': 'gray'
        }

        self.picked_color = 'gray'

        self.ball_buttons = [
            ball_button.Ball(550, 440, 25, 'blue', self.set, 'color_picker_blue'),
            ball_button.Ball(610, 440, 25, 'green', self.set, 'color_picker_green'),
            ball_button.Ball(670, 440, 25, 'red', self.set, 'color_picker_red'),
            ball_button.Ball(730, 440, 25, 'yellow', self.set, 'color_picker_yellow')
        ]

        self.ball_containers = [
            ball_container.Ball(60, 440, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 440, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 440, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 440, 25, 'gray', self.set, 'color_slot_4')
        ]

    def update(self, state, process):
        self.input['send'] = False
        self.input['mouse_pos'] = pygame.mouse.get_pos()
        self.input['LPM'] = pygame.mouse.get_pressed()[0]

        self.display.fill((0, 0, 0))

        if state == "IN-GAME":
            self.reset_ball_buttons()

            for ball in self.ball_buttons + self.ball_containers:
                ball.hoover(self.input['mouse_pos'])

            for ball in self.ball_buttons:
                if ball.intersect():
                    ball.clicked(self.input['LPM'])

            for ball in self.ball_containers:
                if ball.intersect():
                    ball.clicked(self.input['LPM'], self.picked_color)

            if self.input['color_picker_blue']:
                self.picked_color = 'blue'
            elif self.input['color_picker_green']:
                self.picked_color = 'green'
            elif self.input['color_picker_red']:
                self.picked_color = 'red'
            elif self.input['color_picker_yellow']:
                self.picked_color = 'yellow'

            self.button_rect(345, 420, 100, 40, 'green', 'send', "SEND")

            for ball in self.ball_buttons + self.ball_containers:
                ball.draw(self.display)

        process(self.input)

    def set(self, identity, val):
        self.input[identity] = val

    def reset_ball_buttons(self):
        self.input['color_picker_red'] = False
        self.input['color_picker_green'] = False
        self.input['color_picker_blue'] = False
        self.input['color_picker_yellow'] = False

    def reset_ball_containers(self):
        self.input['color_slot_1'] = 'gray'
        self.input['color_slot_2'] = 'gray'
        self.input['color_slot_3'] = 'gray'
        self.input['color_slot_4'] = 'gray'

    def button_rect(self, x, y, w, h, color, target, text):

        small_text = pygame.font.Font(None, 36)
        rendered_text = small_text.render(text, 1, (0, 0, 0))

        if self.intersect(x, y, w=w, h=h):
            pygame.draw.rect(self.display, pygame.Color(color) + pygame.Color(100, 100, 100, 0), (x, y, w, h))
            if self.input['LPM']:
                self.input[target] = True
                self.picked_color = color
        else:
            pygame.draw.rect(self.display, pygame.Color(color) - pygame.Color(50, 50, 50, 0), (x, y, w, h))

        self.display.blit(rendered_text, (x + w / 2 - (18 * 4) / 2, y + (h / 2) - (36 / 2)))

    def intersect(self, x, y, r=None, w=None, h=None):
        if r:
            if np.sqrt((x - self.input['mouse_pos'][0]) ** 2 + (y - self.input['mouse_pos'][1]) ** 2) <= r:
                return True
        elif w and h:
            if x <= self.input['mouse_pos'][0] <= x + w and \
                    y <= self.input['mouse_pos'][1] <= y + h:
                return True

            return False
