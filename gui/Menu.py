import pygame_menu

from gui.WindowState import WindowState


class Menu:

    def __init__(self):
        self.menu = pygame_menu.Menu('Welcome', 600, 600,
                                theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button('PlayRL', self.start_game)
        self.menu.add.button('Play', self.start_testplay)
        self.menu.add.button('Train RL', self.start_training)
        self.menu.add.text_input('Agent: ', 'QTable', onchange=self.set_name)
        self.menu.add.dropselect('Training Mode', [('selfplay', 0), ('random', 1)], 1, onchange=self.set_training_mode)
        self.menu.add.button('Test RL', self.play_random)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.agent_name = "QTable"
        self.window_state = WindowState.MENU
        self.training_mode = 1


    def start_game(self):
        self.window_state = WindowState.PLAY
        self.menu.disable()

    def start_training(self):
        self.window_state = WindowState.TRAINING
        self.menu.disable()

    def set_name(self,name):
        self.agent_name = name

    def set_training_mode(self, value, mode):
        self.training_mode = value[1]
        print(self.training_mode)

    def play_random(self):
        self.window_state = WindowState.TEST
        self.menu.disable()

    def start_testplay(self):
        self.window_state = WindowState.SELF
        self.menu.disable()

    def run(self, win):
        self.menu.mainloop(win)

    def enable(self):
        self.menu.enable()