import pygame


class Input:
    def __init__(self, pyg, state):
        self.pygame = pyg
        self.state = state

    def update(self):
        if self.state:  # determining current game state(for now its boolean(running))
            for event in self.pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = False
