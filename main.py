import communication
import time
import pygame
import input


class Main:
    def __init__(self):
        self.connected = True
        self.running = True

        self.size = self.width, self.height = [800, 600]

        self.Display = pygame.Surface

        self.screen = None
        self.communication_module = None

        self.time_stamp = 0.016  # 60 FPS

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=self.size)
        self.communication_module = communication.ComSupervisor("127.0.0.1", 50001)

        if not self.communication_module.connect():
            self.connected = False
            print("Unable to connect to server %s" % (self.communication_module.get_info(),))

        last_update = 0
        while self.running:
            if time.perf_counter() - last_update >= self.time_stamp:

                self.handle_events()

                if self.connected:
                    data = {
                        'type': 'hi',
                        'value': 'test'
                    }

                    self.communication_module.send(data)

                self.screen.fill((0, 0, 0))
                pygame.display.flip()

                # print(1 / (time.perf_counter() - last_update))
                last_update = time.perf_counter()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


if __name__ == '__main__':
    game = Main()
    game.run()
