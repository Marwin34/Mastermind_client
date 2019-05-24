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

    def reset_state(self):
        self.reset_commands()
        self.data_container['nick'] = None

        self.gui.reset_state()


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
            'quit': False,
            'look_for_opponent': False
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
            elif data['type'] == 'start_game':
                self.table_gui.set_duelers(data['value']['player_1'], data['value']['player_2'])
                self.gui = self.table_gui
            elif data['type'] == 'table_update':
                self.gui.display_table_update(data['value'])
            elif data['type'] == 'game_over':
                self.gui.display_game_over(data['value'])
            elif data['type'] == 'game_leaver':
                if self.gui == self.table_gui:
                    self.gui.display_game_leaver(data['value'])
                else:
                    self.next()

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
                request_value = [
                    self.data_container['color_slot_1'],
                    self.data_container['color_slot_2'],
                    self.data_container['color_slot_3'],
                    self.data_container['color_slot_4']
                ]
                data = {
                    'type': 'picked_colors',
                    'value': request_value
                }

                if 'gray' not in request_value:
                    self.communication.send(data)
                    self.gui.reset_containers()

            elif self.commands['code_init']:
                request_value = [
                    self.data_container['color_slot_1'],
                    self.data_container['color_slot_2'],
                    self.data_container['color_slot_3'],
                    self.data_container['color_slot_4']
                ]
                data = {
                    'type': 'code_init',
                    'value': request_value
                }

                if 'gray' not in request_value:
                    self.communication.send(data)
                    self.gui.reset_containers()

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
        self.commands['code_init'] = False
        self.commands['look_for_opponent'] = False

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
            self.commands['look_for_opponent'] = inputs['look_for_opponent']

            self.data_container['color_slot_1'] = inputs['color_slot_1']
            self.data_container['color_slot_2'] = inputs['color_slot_2']
            self.data_container['color_slot_3'] = inputs['color_slot_3']
            self.data_container['color_slot_4'] = inputs['color_slot_4']

            if self.commands['send'] or self.commands['quit']:
                self.send()

            if self.commands['look_for_opponent']:
                self.next()
                self.gui = self.code_gui

        self.reset_commands()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.commands['quit'] = True

            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                self.m_observer.notify(pygame.mouse.get_pressed(), pygame.mouse.get_pos())

    def reset_state(self):
        self.reset_commands()

        self.code_gui.reset_state()
        self.table_gui.reset_state()

        self.gui = self.code_gui


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

        self.newly_opened = True

    def update(self):
        self.handle_events()
        self.gui.update(self.process_input)

        data = self.communication.receive()

        if self.newly_opened:  # i dont  like it
            self.send()

        if data:
            if data['type'] == 'joined_table' and data['value']:
                self.newly_opened = True
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
            elif self.newly_opened:
                self.newly_opened = False
                print(self.newly_opened)
                data = {
                    'type': 'join_waiters',
                    'value': True
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

    def reset_state(self):
        self.reset_commands()
        self.gui.reset_state()
