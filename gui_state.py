import pygame
import ball_button
import ball_container
import rectangle_button
from observer_type import ObserverType
from abstract_gui_state import GUIState
from text_input import TextInput
import consolas_font


class MainMenuGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.display = display

        self.font_path = "consolas/CONSOLA.TTF"

        self.input = {
            'login': False,
            'nick': "",
            'mouse_pos': (0, 0),
            'mouse_buttons': (0, 0, 0)
        }

        self.rectangle_buttons = [
            rectangle_button.Rectangle(345, 420, 100, 40, 'blue', "LOGIN", consolas_font.consola, 36, self.set, 'login')
        ]

        self.mouse_observer.register(self.rectangle_buttons[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.text_inputs = [
            TextInput(200, 300, 400, 36, consolas_font.consola, 36, self.set, 'nick')
        ]

        self.mouse_observer.register(self.text_inputs[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.text_inputs[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.keyboard_observer.register(self.text_inputs[0].key_pressed)

    def update(self, process):
        process(self.input)
        self.reset_input()

    def draw(self):
        self.display.fill(pygame.Color('green'))

        for rectangle in self.rectangle_buttons:
            rectangle.draw(self.display)

        for text_input in self.text_inputs:
            text_input.draw(self.display)

    def set(self, identity, val):
        self.input[identity] = val

    def reset_input(self):
        self.input['login'] = False


class InGameGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.turn = 1

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
            ball_button.Ball(60, 510, 25, 'blue', self.set, 'color_picker_blue'),
            ball_button.Ball(120, 510, 25, 'green', self.set, 'color_picker_green'),
            ball_button.Ball(180, 510, 25, 'red', self.set, 'color_picker_red'),
            ball_button.Ball(240, 510, 25, 'yellow', self.set, 'color_picker_yellow')
        ]

        for button in self.ball_buttons:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.ball_containers = [
            ball_container.Ball(60, 440, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 440, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 440, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 440, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(60, 380, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 380, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 380, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 380, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(60, 320, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 320, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 320, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 320, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(60, 260, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 260, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 260, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 260, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(60, 200, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(120, 200, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(180, 200, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(240, 200, 25, 'gray', self.set, 'color_slot_4')
        ]

        self.ball_result = [
            ball_container.Ball(300, 440, 25, 'gray', None, None),
            ball_container.Ball(360, 440, 25, 'gray', None, None),
            ball_container.Ball(420, 440, 25, 'gray', None, None),
            ball_container.Ball(480, 440, 25, 'gray', None, None),

            ball_container.Ball(300, 380, 25, 'gray', None, None),
            ball_container.Ball(360, 380, 25, 'gray', None, None),
            ball_container.Ball(420, 380, 25, 'gray', None, None),
            ball_container.Ball(480, 380, 25, 'gray', None, None),

            ball_container.Ball(300, 320, 25, 'gray', None, None),
            ball_container.Ball(360, 320, 25, 'gray', None, None),
            ball_container.Ball(420, 320, 25, 'gray', None, None),
            ball_container.Ball(480, 320, 25, 'gray', None, None),

            ball_container.Ball(300, 260, 25, 'gray', None, None),
            ball_container.Ball(360, 260, 25, 'gray', None, None),
            ball_container.Ball(420, 260, 25, 'gray', None, None),
            ball_container.Ball(480, 260, 25, 'gray', None, None),

            ball_container.Ball(300, 200, 25, 'gray', None, None),
            ball_container.Ball(360, 200, 25, 'gray', None, None),
            ball_container.Ball(420, 200, 25, 'gray', None, None),
            ball_container.Ball(480, 200, 25, 'gray', None, None)
        ]

        self.opponent_balls = [
            ball_container.Ball(560, 440, 25, 'gray', None, None),
            ball_container.Ball(620, 440, 25, 'gray', None, None),
            ball_container.Ball(680, 440, 25, 'gray', None, None),
            ball_container.Ball(740, 440, 25, 'gray', None, None),

            ball_container.Ball(560, 380, 25, 'gray', None, None),
            ball_container.Ball(620, 380, 25, 'gray', None, None),
            ball_container.Ball(680, 380, 25, 'gray', None, None),
            ball_container.Ball(740, 380, 25, 'gray', None, None),

            ball_container.Ball(560, 320, 25, 'gray', None, None),
            ball_container.Ball(620, 320, 25, 'gray', None, None),
            ball_container.Ball(680, 320, 25, 'gray', None, None),
            ball_container.Ball(740, 320, 25, 'gray', None, None),

            ball_container.Ball(560, 260, 25, 'gray', None, None),
            ball_container.Ball(620, 260, 25, 'gray', None, None),
            ball_container.Ball(680, 260, 25, 'gray', None, None),
            ball_container.Ball(740, 260, 25, 'gray', None, None),

            ball_container.Ball(560, 200, 25, 'gray', None, None),
            ball_container.Ball(620, 200, 25, 'gray', None, None),
            ball_container.Ball(680, 200, 25, 'gray', None, None),
            ball_container.Ball(740, 200, 25, 'gray', None, None)
        ]

        for ball in self.ball_containers:
            ball.disable()

        self.active_row()

        for button in self.ball_containers:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.rectangle_buttons = [
            rectangle_button.Rectangle(345, 510, 100, 40, 'green', "SEND", consolas_font.consola, 36, self.set, 'send')
        ]

        self.mouse_observer.register(self.rectangle_buttons[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

    def update(self, process):
        if self.input['color_picker_blue']:
            self.picked_color = 'blue'
        elif self.input['color_picker_green']:
            self.picked_color = 'green'
        elif self.input['color_picker_red']:
            self.picked_color = 'red'
        elif self.input['color_picker_yellow']:
            self.picked_color = 'yellow'

        for ball in self.ball_containers:
            ball.expect_color(self.picked_color)

        process(self.input)
        self.reset_input()

    def draw(self):
        self.display.fill(pygame.Color('cyan'))

        for ball in self.ball_buttons + self.ball_containers + self.ball_result + self.opponent_balls:
            ball.draw(self.display)

        for rectangle in self.rectangle_buttons:
            rectangle.draw(self.display)

    def set(self, identity, val):
        self.input[identity] = val

    def reset_input(self):
        self.input['send'] = False
        self.input['color_picker_red'] = False
        self.input['color_picker_green'] = False
        self.input['color_picker_blue'] = False
        self.input['color_picker_yellow'] = False

    def reset_containers(self):
        self.input['color_slot_1'] = 'gray'
        self.input['color_slot_2'] = 'gray'
        self.input['color_slot_3'] = 'gray'
        self.input['color_slot_4'] = 'gray'

    def active_row(self):
        if self.turn < 6:
            for i in range((self.turn - 1) * 4, self.turn * 4):
                self.ball_containers[i].enable()

        if self.turn > 1:
            for i in range((self.turn - 2) * 4, (self.turn - 1) * 4):
                self.ball_containers[i].disable()

    def display_response(self, response):
        i = (self.turn - 1) * 4
        print(response['result'])
        for color in response['result']:
            self.ball_result[i].set_color(color)
            i += 1

        j = (self.turn - 1) * 4
        for color in response['opponent']:
            self.opponent_balls[j].set_color(color)
            j += 1

        self.turn = response['turn']
        self.active_row()


class CodeDefineGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.display = display

        self.message_text = "Pick code for opponent."

        self.message_x = 400 - len(self.message_text) / 2 * 27
        self.message_y = 300 - 50 / 2

        self.text = pygame.font.Font(consolas_font.consola, 50)
        self.rendered_text = self.text.render(self.message_text, 1, (pygame.Color('black')))

        self.input = {
            'code_init': False,
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
            rectangle_button.Rectangle(345, 420, 100, 40, 'green', "CONFIRM", consolas_font.consola, 36, self.set,
                                       'code_init')
        ]

        self.mouse_observer.register(self.rectangle_buttons[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

    def update(self, process):
        if self.input['color_picker_blue']:
            self.picked_color = 'blue'
        elif self.input['color_picker_green']:
            self.picked_color = 'green'
        elif self.input['color_picker_red']:
            self.picked_color = 'red'
        elif self.input['color_picker_yellow']:
            self.picked_color = 'yellow'

        for ball in self.ball_containers:
            ball.expect_color(self.picked_color)

        process(self.input)
        self.reset_input()

    def draw(self):
        self.display.fill(pygame.Color('blue'))

        self.display.blit(self.rendered_text, (self.message_x, self.message_y))

        for ball in self.ball_buttons + self.ball_containers:
            ball.draw(self.display)

        for rectangle in self.rectangle_buttons:
            rectangle.draw(self.display)

    def set(self, identity, val):
        self.input[identity] = val

    def reset_input(self):
        self.input['code_init'] = False
        self.input['color_picker_red'] = False
        self.input['color_picker_green'] = False
        self.input['color_picker_blue'] = False
        self.input['color_picker_yellow'] = False

    def reset_containers(self):
        self.input['color_slot_1'] = 'gray'
        self.input['color_slot_2'] = 'gray'
        self.input['color_slot_3'] = 'gray'
        self.input['color_slot_4'] = 'gray'


class WaitingForOpponentGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.message_text = "WAITING FOR OPPONENT ..."

        self.message_x = 400 - len(self.message_text) / 2 * 27
        self.message_y = 300 - 50 / 2

        self.display = display

        self.text = pygame.font.Font(consolas_font.consola, 50)
        self.rendered_text = self.text.render(self.message_text, 1, (pygame.Color('black')))

    def update(self, process):
        process(None)

    def draw(self):
        self.display.fill(pygame.Color('blue'))

        self.display.blit(self.rendered_text, (self.message_x, self.message_y))

    def set(self, identity, val):
        pass

    def reset_input(self):
        pass
