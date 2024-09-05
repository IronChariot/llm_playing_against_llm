class GameManager:
    def __init__(self, game):
        self.game = game

    def run_game(self):
        self.game.play_match()