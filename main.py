import communication
import time
import pygame
import gui


class Main:
    def __init__(self):
        self.connected = True
        self.running = True

        self.size = self.width, self.height = [800, 600]

        self.display = pygame.Surface

        self.communication_module = None

        self.time_stamp = 0.016  # 60 FPS

        self.gui = None

        self.picked_colors = [None, None, None, None]

    def run(self):
        pygame.init()
        self.display = pygame.display.set_mode(size=self.size)

        self.gui = gui.GUI(self.display)

        self.communication_module = communication.ComSupervisor("127.0.0.1", 50001)

        if not self.communication_module.connect():
            self.connected = False
            print("Unable to connect to server %s" % (self.communication_module.get_info(),))

        last_update = 0
        while self.running:
            if time.perf_counter() - last_update >= self.time_stamp:
                self.handle_events()

                self.gui.update("IN-GAME", self.process_input)
                pygame.display.flip()

                # print(1 / (time.perf_counter() - last_update))
                last_update = time.perf_counter()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
