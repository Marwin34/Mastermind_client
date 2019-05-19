class KeyboardObserver:
    def __init__(self):
        self.buttons_state_changes = []

    def register(self, function):
        self.buttons_state_changes.append(function)

    def notify(self, key_pressed):
        for function in self.buttons_state_changes:
            function(key_pressed)
