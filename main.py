import communication
import time
import pygame
from game_states import MainMenu, WaitingForOpponent, InGame
from game_state_type import StateType


class Main:
    def __init__(self):
        pygame.init()
        self.connected = True
        self.running = True

        self.size = self.width, self.height = [800, 600]

        self.display = pygame.Surface
        self.display = pygame.display.set_mode(size=self.size)

        self.communication_module = communication.ComSupervisor("127.0.0.1", 50001)

        self.time_stamp = 0.016  # 60 FPS

        self.picked_colors = [None, None, None, None]

        self.main_menu_state = MainMenu(self.quit, self.change_state, StateType.MAIN_MENU, self.display,
                                        self.communication_module)

        self.waiting_for_opponent_state = WaitingForOpponent(self.quit, self.change_state,
                                                             StateType.WAITING_FOR_OPPONENT, self.display,
                                                             self.communication_module)

        self.in_game_state = InGame(self.quit, self.change_state, StateType.IN_GAME, self.display,
                                    self.communication_module)

        self.active_state = self.main_menu_state

    def run(self):
        last_update = 0
        while self.running:
            if time.perf_counter() - last_update >= self.time_stamp:
                self.active_state.update()
                self.active_state.draw()
                pygame.display.flip()

                # print(1 / (time.perf_counter() - last_update))
                last_update = time.perf_counter()

        pygame.quit()

    def change_state(self, state_type):
        self.active_state.reset_state()
        if state_type == StateType.MAIN_MENU:
            self.active_state = self.waiting_for_opponent_state
        elif state_type == StateType.WAITING_FOR_OPPONENT:
            self.active_state = self.in_game_state
        elif state_type == StateType.IN_GAME:
            self.active_state = self.waiting_for_opponent_state

    def quit(self):
        self.running = False

    def process_input(self, inputs):
        self.picked_colors = [
            inputs['color_slot_1'],
            inputs['color_slot_2'],
            inputs['color_slot_3'],
            inputs['color_slot_4']
        ]

        if inputs['send']:
            self.send()

    def send(self):
        if self.connected:
            data = {
                'type': 'colors_match',
                'value': self.picked_colors
            }

            self.communication_module.send(data)
        else:
            print("Disconnected.")


if __name__ == '__main__':
    game = Main()
    game.run()
