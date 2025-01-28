import pygame_menu

from Checkers_template.WindowState import WindowState


class Menu:

    def __init__(self):
        self.menu = pygame_menu.Menu('Welcome', 400, 300,
                                theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button('PlayRL', self.start_game)
        self.menu.add.button('Play', self.start_testplay)
        self.menu.add.button('Train RL', self.start_training)
        self.menu.add.text_input('Agent: ', 'QTable', onchange=self.get_name)
        self.menu.add.button('Test RL', self.play_random)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.agent_Name = "QTable"
        self.window_state = WindowState.MENU


    def start_game(self):
        self.window_state = WindowState.PLAY
        self.menu.disable()

    def start_training(self):
        self.window_state = WindowState.TRAINING
        self.menu.disable()

    def get_name(self,value):
        self.agent_Name = value

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