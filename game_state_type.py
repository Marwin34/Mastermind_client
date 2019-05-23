from enum import Enum


class StateType(Enum):
    MAIN_MENU = 1
    WAITING_FOR_OPPONENT = 2
    IN_GAME = 3
