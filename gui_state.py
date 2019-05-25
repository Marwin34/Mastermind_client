import pygame
import ball_button
import ball_container
import rectangle_button
from observer_type import ObserverType
from abstract_gui_state import GUIState
from text_input import TextInput
import consolas_font
import display_settings


# TODO better graphics, send key bug sfter reentering queue, displaying players info


class MainMenuGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.display = display

        self.font_path = "consolas/CONSOLA.TTF"

        self.input = {
            'login': False,
            'nick': ""
        }

        self.rectangle_buttons = [
            rectangle_button.Rectangle(display_settings.display_width / 2, 420, 'blue', "LOGIN", consolas_font.consola,
                                       36, self.set, 'login')
        ]

        self.mouse_observer.register(self.rectangle_buttons[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.text_inputs = [
            TextInput(display_settings.display_width / 2 - 400 / 2, 300, 400, 36, consolas_font.consola, 36, self.set,
                      'nick')
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

    def reset_state(self):
        self.reset_input()
        for text_input in self.text_inputs:
            text_input.reset_value()


class InGameGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.turn = 1

        self.display = display

        self.player_1 = ""
        self.player_2 = ""

        self.text = pygame.font.Font(consolas_font.consola, 32)
        self.rendered_player_1 = self.text.render("", 1, (pygame.Color('black')))
        self.rendered_player_2 = self.text.render("", 1, (pygame.Color('black')))

        self.rendered_player_1_pos_x = 0
        self.rendered_player_1_pos_y = 0

        self.rendered_player_2_pos_x = 0
        self.rendered_player_2_pos_y = 0

        self.rendered_outcome_pos_x = 0
        self.rendered_outcome_pos_y = 0

        self.game_over_message = ""

        self.text = pygame.font.Font(consolas_font.consola, 40)
        self.rendered_outcome = self.text.render("", 1, (pygame.Color('black')))

        self.background = pygame.image.load("images/in_game_bg_2.png")
        self.background_rect = self.background.get_rect()

        self.input = {
            'send': False,
            'look_for_opponent': False,
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
            ball_button.Ball(130, 600, 25, 'blue', self.set, 'color_picker_blue'),
            ball_button.Ball(190, 600, 25, 'green', self.set, 'color_picker_green'),
            ball_button.Ball(250, 600, 25, 'red', self.set, 'color_picker_red'),
            ball_button.Ball(310, 600, 25, 'yellow', self.set, 'color_picker_yellow')
        ]

        for button in self.ball_buttons:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.ball_containers = [
            ball_container.Ball(130, 520, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 520, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 520, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 520, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 460, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 460, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 460, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 460, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 400, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 400, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 400, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 400, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 340, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 340, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 340, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 340, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 280, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 280, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 280, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 280, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 220, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 220, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 220, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 220, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 160, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 160, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 160, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 160, 25, 'gray', self.set, 'color_slot_4'),

            ball_container.Ball(130, 100, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(190, 100, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(250, 100, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(310, 100, 25, 'gray', self.set, 'color_slot_4')
        ]

        self.ball_result = [
            ball_container.Ball(390, 520, 25, 'gray', None, None),
            ball_container.Ball(450, 520, 25, 'gray', None, None),
            ball_container.Ball(510, 520, 25, 'gray', None, None),
            ball_container.Ball(570, 520, 25, 'gray', None, None),

            ball_container.Ball(390, 460, 25, 'gray', None, None),
            ball_container.Ball(450, 460, 25, 'gray', None, None),
            ball_container.Ball(510, 460, 25, 'gray', None, None),
            ball_container.Ball(570, 460, 25, 'gray', None, None),

            ball_container.Ball(390, 400, 25, 'gray', None, None),
            ball_container.Ball(450, 400, 25, 'gray', None, None),
            ball_container.Ball(510, 400, 25, 'gray', None, None),
            ball_container.Ball(570, 400, 25, 'gray', None, None),

            ball_container.Ball(390, 340, 25, 'gray', None, None),
            ball_container.Ball(450, 340, 25, 'gray', None, None),
            ball_container.Ball(510, 340, 25, 'gray', None, None),
            ball_container.Ball(570, 340, 25, 'gray', None, None),

            ball_container.Ball(390, 280, 25, 'gray', None, None),
            ball_container.Ball(450, 280, 25, 'gray', None, None),
            ball_container.Ball(510, 280, 25, 'gray', None, None),
            ball_container.Ball(570, 280, 25, 'gray', None, None),

            ball_container.Ball(390, 220, 25, 'gray', None, None),
            ball_container.Ball(450, 220, 25, 'gray', None, None),
            ball_container.Ball(510, 220, 25, 'gray', None, None),
            ball_container.Ball(570, 220, 25, 'gray', None, None),

            ball_container.Ball(390, 160, 25, 'gray', None, None),
            ball_container.Ball(450, 160, 25, 'gray', None, None),
            ball_container.Ball(510, 160, 25, 'gray', None, None),
            ball_container.Ball(570, 160, 25, 'gray', None, None),

            ball_container.Ball(390, 100, 25, 'gray', None, None),
            ball_container.Ball(450, 100, 25, 'gray', None, None),
            ball_container.Ball(510, 100, 25, 'gray', None, None),
            ball_container.Ball(570, 100, 25, 'gray', None, None)
        ]

        self.opponent_balls = [
            ball_container.Ball(714, 520, 25, 'gray', None, None),
            ball_container.Ball(774, 520, 25, 'gray', None, None),
            ball_container.Ball(834, 520, 25, 'gray', None, None),
            ball_container.Ball(894, 520, 25, 'gray', None, None),

            ball_container.Ball(714, 460, 25, 'gray', None, None),
            ball_container.Ball(774, 460, 25, 'gray', None, None),
            ball_container.Ball(834, 460, 25, 'gray', None, None),
            ball_container.Ball(894, 460, 25, 'gray', None, None),

            ball_container.Ball(714, 400, 25, 'gray', None, None),
            ball_container.Ball(774, 400, 25, 'gray', None, None),
            ball_container.Ball(834, 400, 25, 'gray', None, None),
            ball_container.Ball(894, 400, 25, 'gray', None, None),

            ball_container.Ball(714, 340, 25, 'gray', None, None),
            ball_container.Ball(774, 340, 25, 'gray', None, None),
            ball_container.Ball(834, 340, 25, 'gray', None, None),
            ball_container.Ball(894, 340, 25, 'gray', None, None),

            ball_container.Ball(714, 280, 25, 'gray', None, None),
            ball_container.Ball(774, 280, 25, 'gray', None, None),
            ball_container.Ball(834, 280, 25, 'gray', None, None),
            ball_container.Ball(894, 280, 25, 'gray', None, None),

            ball_container.Ball(714, 220, 25, 'gray', None, None),
            ball_container.Ball(774, 220, 25, 'gray', None, None),
            ball_container.Ball(834, 220, 25, 'gray', None, None),
            ball_container.Ball(894, 220, 25, 'gray', None, None),

            ball_container.Ball(714, 160, 25, 'gray', None, None),
            ball_container.Ball(774, 160, 25, 'gray', None, None),
            ball_container.Ball(834, 160, 25, 'gray', None, None),
            ball_container.Ball(894, 160, 25, 'gray', None, None),

            ball_container.Ball(714, 100, 25, 'gray', None, None),
            ball_container.Ball(774, 100, 25, 'gray', None, None),
            ball_container.Ball(834, 100, 25, 'gray', None, None),
            ball_container.Ball(894, 100, 25, 'gray', None, None)
        ]

        for ball in self.ball_containers:
            ball.disable()

        self.active_row()

        for button in self.ball_containers:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.rectangle_buttons = [
            rectangle_button.Rectangle(512, 630, 'green', "CHECK", consolas_font.consola, 36, self.set, 'send'),
            rectangle_button.Rectangle(512, 690, 'red', "AGAIN", consolas_font.consola, 36,
                                       self.set, 'look_for_opponent')
        ]

        self.mouse_observer.register(self.rectangle_buttons[0].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[0].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.mouse_observer.register(self.rectangle_buttons[1].hoover, ObserverType.MOUSE_POS_CHANGES)
        self.mouse_observer.register(self.rectangle_buttons[1].clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.rectangle_buttons[1].hide()
        self.rectangle_buttons[1].disable()

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

        self.display.blit(self.background, self.background_rect)

        for ball in self.ball_buttons + self.ball_containers + self.ball_result + self.opponent_balls:
            ball.draw(self.display)

        for rectangle in self.rectangle_buttons:
            rectangle.draw(self.display)

        self.display.blit(self.rendered_player_1, (self.rendered_player_1_pos_x, self.rendered_player_1_pos_y))
        self.display.blit(self.rendered_player_2, (self.rendered_player_2_pos_x, self.rendered_player_2_pos_y))

        self.display.blit(self.rendered_outcome, (self.rendered_outcome_pos_x, self.rendered_outcome_pos_y))

    def set(self, identity, val):
        self.input[identity] = val

    def reset_input(self):
        self.input['send'] = False
        self.input['look_for_opponent'] = False
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
        if self.turn < 9:
            for i in range((self.turn - 1) * 4, self.turn * 4):
                self.ball_containers[i].enable()

        if self.turn > 1:
            for i in range((self.turn - 2) * 4, (self.turn - 1) * 4):
                self.ball_containers[i].disable()

    def display_table_update(self, response):
        i = (self.turn - 1) * 4
        for color in response['result']:
            self.ball_result[i].set_color(color)
            i += 1

        j = (self.turn - 1) * 4
        for color in response['opponent']:
            self.opponent_balls[j].set_color(color)
            j += 1

        self.turn = response['turn']
        self.active_row()

    def display_game_over(self, response):
        self.rectangle_buttons[0].disable()
        self.rectangle_buttons[0].hide()

        self.rectangle_buttons[1].enable()
        self.rectangle_buttons[1].show()

        i = (self.turn - 1) * 4
        for color in response['result']:
            self.ball_result[i].set_color(color)
            i += 1

        j = (self.turn - 1) * 4
        for color in response['opponent']:
            self.opponent_balls[j].set_color(color)
            j += 1

        for k in range((self.turn - 1) * 4, self.turn * 4):
            self.ball_containers[k].disable()

        if response['outcome'] == 'winner':
            self.game_over_message = "You win!"
            self.rendered_outcome = self.text.render("You win!", 1, (pygame.Color('green')))
        elif response['outcome'] == 'loser':
            self.game_over_message = "You lost!"
            self.rendered_outcome = self.text.render("You lost!", 1, (pygame.Color('red')))
        elif response['outcome'] == 'withdraw':
            self.game_over_message = "Withdraw!"
            self.rendered_outcome = self.text.render("Withdraw!", 1, (pygame.Color('black')))

        self.rendered_outcome_pos_x = display_settings.display_width / 2 - len(self.game_over_message) * 31
        self.rendered_outcome_pos_y = display_settings.display_height / 2 - 40 / 2

    def display_game_leaver(self, response):
        self.rectangle_buttons[0].disable()
        self.rectangle_buttons[0].hide()

        self.rectangle_buttons[1].enable()
        self.rectangle_buttons[1].show()

        for k in range((self.turn - 1) * 4, self.turn * 4):
            self.ball_containers[k].disable()

        if response['outcome'] == 'winner':
            self.game_over_message = "You won!"
            self.rendered_outcome = self.text.render("You won!", 1, (pygame.Color('green')))

        self.rendered_outcome_pos_x = display_settings.display_width / 2 - len(self.game_over_message) * 31
        self.rendered_outcome_pos_y = display_settings.display_height / 2 - 40 / 2

    def set_duelers(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        self.rendered_player_1 = self.text.render(self.player_1, 1, (pygame.Color('black')))
        self.rendered_player_2 = self.text.render(self.player_2, 1, (pygame.Color('black')))

        self.rendered_player_1_pos_x = 130
        self.rendered_player_1_pos_y = 10

        self.rendered_player_2_pos_x = 714
        self.rendered_player_2_pos_y = 10

    def reset_state(self):
        self.reset_input()
        self.reset_containers()

        self.picked_color = 'gray'

        self.player_1 = ""
        self.player_2 = ""

        self.rendered_player_1 = self.text.render("", 1, (pygame.Color('black')))
        self.rendered_player_2 = self.text.render("", 1, (pygame.Color('black')))

        self.rendered_player_1_pos_x = 0
        self.rendered_player_1_pos_y = 0

        self.rendered_player_2_pos_x = 0
        self.rendered_player_2_pos_y = 0

        self.rendered_outcome_pos_x = 0
        self.rendered_outcome_pos_y = 0

        self.game_over_message = ""

        self.text = pygame.font.Font(consolas_font.consola, 40)
        self.rendered_outcome = self.text.render("", 1, (pygame.Color('black')))

        self.turn = 1

        for ball in self.ball_containers:
            ball.disable()

        self.active_row()

        for ball in self.ball_containers + self.ball_result + self.opponent_balls:
            ball.reset_value()

        self.rectangle_buttons[0].show()
        self.rectangle_buttons[0].enable()

        self.rectangle_buttons[1].hide()
        self.rectangle_buttons[1].disable()


class CodeDefineGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.display = display

        self.message_text = "Pick code for opponent."

        self.message_x = display_settings.display_width / 2 - len(self.message_text) / 2 * 26
        self.message_y = 260 - 50 / 2

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
            ball_button.Ball(422, 520, 25, 'blue', self.set, 'color_picker_blue'),
            ball_button.Ball(482, 520, 25, 'green', self.set, 'color_picker_green'),
            ball_button.Ball(542, 520, 25, 'red', self.set, 'color_picker_red'),
            ball_button.Ball(602, 520, 25, 'yellow', self.set, 'color_picker_yellow')
        ]

        for button in self.ball_buttons:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.ball_containers = [
            ball_container.Ball(422, 440, 25, 'gray', self.set, 'color_slot_1'),
            ball_container.Ball(482, 440, 25, 'gray', self.set, 'color_slot_2'),
            ball_container.Ball(542, 440, 25, 'gray', self.set, 'color_slot_3'),
            ball_container.Ball(602, 440, 25, 'gray', self.set, 'color_slot_4')
        ]

        for button in self.ball_containers:
            self.mouse_observer.register(button.hoover, ObserverType.MOUSE_POS_CHANGES)
            self.mouse_observer.register(button.clicked, ObserverType.MOUSE_BUTTONS_CHANGES)

        self.rectangle_buttons = [
            rectangle_button.Rectangle(display_settings.display_width / 2, 600, 'green', "CONFIRM",
                                       consolas_font.consola, 36, self.set,
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

    def reset_state(self):
        self.reset_input()
        self.reset_containers()

        self.picked_color = 'gray'

        for ball in self.ball_containers:
            ball.reset_value()


class WaitingForOpponentGUI(GUIState):
    def __init__(self, display, mouse_observer=None, keyboard_observer=None):
        self.mouse_observer = mouse_observer
        self.keyboard_observer = keyboard_observer

        self.message_text = "Waiting for opponent."

        self.message_x = display_settings.display_width / 2 - len(self.message_text) / 2 * 27
        self.message_y = display_settings.display_height / 2 - 50 / 2

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

    def reset_state(self):
        pass
