from abstract_game_state import GameState
from gui_state import MainMenuGUI, WaitingForOpponentGUI, InGameGUI, CodeDefineGUI
import pygame
from mouse_observer import MouseObserver
from keyboard_observer import KeyboardObserver


class MainMenu(GameState):
    def __init__(self, quit_callback, change_state_callback, state_type, display, communication_module):
        self.quit_callback = quit_callback
        self.change_state_callback = change_state_callback
        self.state_type = state_type
        self.display = display
        self.communication = communication_module

        self.connected = self.communication.connect()

        self.m_observer = MouseObserver()
        self.k_observer = KeyboardObserver()

        self.gui = MainMenuGUI(self.display, self.m_observer, self.k_observer)

        self.commands = {
            'login': False,
            'quit': False
        }

        self.data_container = {
            'nick': None
        }

    def update(self):
        self.handle_events()
        self.gui.update(self.process_input)

        data = self.communication.receive()

        if data:
            if data['type'] == 'server_response' and data['value']:
                self.next()
            elif data['type'] == 'quit':
                self.quit_callback()

    def draw(self):
        self.gui.draw()

    def send(self):
        if not self.connected:
            print("You aren't connected to server. Trying to connect.")
            if self.communication.connect():
                print("Connection established.")
                self.send()
            else:
                print("Unable to connect to server, check your internet connection or try again later.")
        else:
            if self.commands['login']:
                data = {
                    'type': 'login',
                    'value': self.data_container['nick']
                }
            else:
                data = {
                    'type': 'quit',
                    'value': 'quit_request'
                }

            self.communication.send(data)

    def next(self):
        self.change_state_callback(self.state_type)

    def reset_commands(self):
        self.commands['login'] = False
        self.commands['quit'] = False

    def process_input(self, inputs):
        self.commands['login'] = inputs['login']

        self.data_container['nick'] = inputs['nick']

        if self.commands['login'] or self.commands['quit']:
            self.send()

        self.reset_commands()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.commands['quit'] = True

            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                self.m_observer.notify(pygame.mouse.get_pressed(), pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                self.k_observer.notify((event.key, event.unicode))


class InGame(GameState):
    def __init__(self, quit_callback, change_state_callback, state_type, display, communication_module):
        self.m_observer = MouseObserver()

        self.quit_callback = quit_callback
        self.change_state_callback = change_state_callback
        self.state_type = state_type
        self.display = display
        self.code_gui = CodeDefineGUI(self.display, self.m_observer)
        self.table_gui = InGameGUI(self.display, self.m_observer)
        self.gui = self.code_gui
        self.communication = communication_module

        self.commands = {
            'send': False,
            'code_init': False,
            'quit': False
        }

        self.data_container = {
            'color_slot_1': 'gray',
            'color_slot_2': 'gray',
            'color_slot_3': 'gray',
            'color_slot_4': 'gray'
        }

    def update(self):
        self.handle_events()
        self.gui.update(self.process_input)

        data = self.communication.receive()

        if data:
            if data['type'] == 'quit':
                self.quit_callback()
            if data['type'] == 'start_game':
                self.gui = self.table_gui

    def draw(self):
        self.gui.draw()

    def send(self):
        if not self.communication.get_info()[2]:
            print("You aren't connected to server. Trying to connect.")
            if self.communication.connect():
                print("Connection established.")
                self.send()
            else:
                print("Unable to connect to server, check your internet connection or try again later.")
        else:
            if self.commands['send']:
                data = {
                    'type': 'picked_colors',
                    'value': [
                        self.data_container['color_slot_1'],
                        self.data_container['color_slot_2'],
                        self.data_container['color_slot_3'],
                        self.data_container['color_slot_4']
                    ]
                }

                self.communication.send(data)
            elif self.commands['code_init']:
                color_1 = self.data_container['color_slot_1']
                color_2 = self.data_container['color_slot_2']
                color_3 = self.data_container['color_slot_3']
                color_4 = self.data_container['color_slot_4']

                if color_1 != 'gray' and color_2 != 'gray' and color_3 != 'gray' and color_4 != 'gray':
                    data = {
                        'type': 'code_init',
                        'value': [color_1, color_2, color_3, color_4]
                    }

                    print(data)
                    self.communication.send(data)

            else:
                data = {
                    'type': 'quit',
                    'value': 'quit_request'
                }

                self.communication.send(data)

    def next(self):
        self.change_state_callback(self.state_type)

    def reset_commands(self):
        self.commands['send'] = False
        self.commands['quit'] = False

        self.data_container['color_slot_1'] = 'gray'
        self.data_container['color_slot_2'] = 'gray'
        self.data_container['color_slot_3'] = 'gray'
        self.data_container['color_slot_4'] = 'gray'

    def process_input(self, inputs):
        if self.gui == self.code_gui:
            self.commands['code_init'] = inputs['code_init']

            self.data_container['color_slot_1'] = inputs['color_slot_1']
            self.data_container['color_slot_2'] = inputs['color_slot_2']
            self.data_container['color_slot_3'] = inputs['color_slot_3']
            self.data_container['color_slot_4'] = inputs['color_slot_4']

            if self.commands['code_init'] or self.commands['quit']:
                self.send()
        else:
            self.commands['send'] = inputs['send']

            self.data_container['color_slot_1'] = inputs['color_slot_1']
            self.data_container['color_slot_2'] = inputs['color_slot_2']
            self.data_container['color_slot_3'] = inputs['color_slot_3']
            self.data_container['color_slot_4'] = inputs['color_slot_4']

            if self.commands['send'] or self.commands['quit']:
                self.send()

        self.reset_commands()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.commands['quit'] = True

            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                self.m_observer.notify(pygame.mouse.get_pressed(), pygame.mouse.get_pos())


class WaitingForOpponent(GameState):
    def __init__(self, quit_callback, change_state_callback, state_type, display, communication_module):
        self.quit_callback = quit_callback
        self.change_state_callback = change_state_callback
        self.state_type = state_type
        self.display = display
        self.communication = communication_module

        self.gui = WaitingForOpponentGUI(self.display)

        self.commands = {
            'quit': False
        }

    def update(self):
        self.handle_events()
        self.gui.update(self.process_input)

        data = self.communication.receive()

        if data:
            if data['type'] == 'joined_table' and data['value']:
                self.next()
            elif data['type'] == 'quit':
                self.quit_callback()

    def draw(self):
        self.gui.draw()

    def send(self):
        if not self.communication.get_info()[2]:
            print("You aren't connected to server. Trying to connect.")
            if self.communication.connect():
                print("Connection established.")
                self.send()
            else:
                print("Unable to connect to server, check your internet connection or try again later.")
        else:
            if self.commands['quit']:
                data = {
                    'type': 'quit',
                    'value': 'quit_request'
                }

                self.communication.send(data)

    def next(self):
        self.change_state_callback(self.state_type)

    def reset_commands(self):
        self.commands['quit'] = False

    def process_input(self, inputs):
        if self.commands['quit']:
            self.send()

        self.reset_commands()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.commands['quit'] = True
