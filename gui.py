import pygame
import ball_button
import ball_container
import mouse_observer
import rectangle_button
from observer_type import ObserverType


class GUI:
    def __init__(self, display):
        self.mouse_observer = mouse_observer.MouseObserver()

        self.display = display

        self.input = {
            'send': False,
            'mouse_pos': (0, 0),
            'mouse_buttons': (0, 0, 0),
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

        for button in self.ball_buttons:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.ball_containers = [
            ball_container.Ball(60, 440, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 440, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 440, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 440, 25, 'gray', self.set, 'color_slot_4')
        ]

        for button in self.ball_containers:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.rectangle_buttons = [
            rectangle_button.Rectangle(345, 420, 100, 40, 'green', "SEND", None, 36, self.set, 'send')
        ]

        self.mouse_observer.register(self.rectangle_buttons[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

    def update(self, state, process):
        self.input['send'] = False
        self.input['mouse_pos'] = pygame.mouse.get_pos()
        self.input['mouse_buttons'] = pygame.mouse.get_pressed()

        self.display.fill((0, 0, 0))

        if state == "IN-GAME":
            self.reset_ball_buttons()

            self.mouse_observer.notify(self.input['mouse_buttons'], self.input['mouse_pos'])

            if self.input['color_picker_blue']:
                self.picked_color = 'blue'
            elif self.input['color_picker_green']:
                self.picked_color = 'green'
            elif self.input['color_picker_red']:
                self.picked_color = 'red'
            elif self.input['color_picker_yellow']:
                self.picked_color = 'yellow'
            elif self.input['send']:
                self.input['send'] = True

            for ball in self.ball_containers:
                ball.expect_color(self.picked_color)

            for ball in self.ball_buttons + self.ball_containers:
                ball.draw(self.display)

            for rectangle in self.rectangle_buttons:
                rectangle.draw(self.display)

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
