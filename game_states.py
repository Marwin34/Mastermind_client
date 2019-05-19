from abstract_game_state import GameState
from gui_state import MainMenuGUI, InGameGUI
import pygame
from mouse_observer import MouseObserver
from keyboard_observer import KeyboardObserver


class MainMenu(GameState):
    def __init__(self, quit_callback, change_state_callback, state_type, display):
        self.quit_callback = quit_callback
        self.change_state_callback = change_state_callback
        self.state_type = state_type
        self.display = display

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

    def draw(self):
        self.gui.draw()

    def send(self):
        pass

    def next(self):
        self.change_state_callback(self.state_type)

    def process_input(self, inputs):
        self.commands['login'] = False
        self.commands['quit'] = False

        self.data_container['nick'] = None

        self.commands['login'] = inputs['login']
        self.commands['quit'] = inputs['quit']

        if self.commands['login']:
            self.next()

        self.data_container['nick'] = inputs['nick']

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_callback()

            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                self.m_observer.notify(pygame.mouse.get_pressed(), pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                self.k_observer.notify((event.key, event.unicode))


class InGame(GameState):
    def __init__(self, quit_callback, change_state_callback, state_type, display):
        self.m_observer = MouseObserver()

        self.quit_callback = quit_callback
        self.change_state_callback = change_state_callback
        self.state_type = state_type
        self.display = display
        self.gui = InGameGUI(self.display, self.m_observer)

        self.commands = {
            'send': False
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

    def draw(self):
        self.gui.draw()

    def send(self):
        pass

    def next(self):
        self.change_state_callback(self.state_type)

    def process_input(self, inputs):
        self.commands['send'] = False
        self.commands['quit'] = False

        self.data_container['color_slot_1'] = 'gray'
        self.data_container['color_slot_2'] = 'gray'
        self.data_container['color_slot_3'] = 'gray'
        self.data_container['color_slot_4'] = 'gray'

        self.commands['send'] = inputs['send']
        self.commands['quit'] = inputs['quit']

        self.data_container['color_slot_1'] = inputs['color_slot_1']
        self.data_container['color_slot_2'] = inputs['color_slot_2']
        self.data_container['color_slot_3'] = inputs['color_slot_3']
        self.data_container['color_slot_4'] = inputs['color_slot_4']

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_callback()

            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                self.m_observer.notify(pygame.mouse.get_pressed(), pygame.mouse.get_pos())
