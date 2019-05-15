from observer_type import ObserverType


class MouseObserver:
    def __init__(self):
        self.mouse_pos_change_targets = []
        self.mouse_buttons_change_targets = []

    def register(self, function, target_type):
        if target_type == ObserverType.MOUSE_BUTTONS_CHANGES:
            self.mouse_buttons_change_targets.append(function)
        elif target_type == ObserverType.MOUSE_POS_CHANGES:
            self.mouse_pos_change_targets.append(function)

    def notify(self, mouse_buttons_state, mouse_pos):
        for function in self.mouse_pos_change_targets:
            function(mouse_pos)

        for function in self.mouse_buttons_change_targets:
            function(mouse_buttons_state)
