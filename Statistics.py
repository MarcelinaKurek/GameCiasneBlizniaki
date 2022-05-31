
class Statistics:

    def __init__(self):
        self.num_of_games = 0
        self.no_twins = 0
        self.twins = 0
        self.moves = 0
        self.max_moves = 0

    def update(self, twin, moves, max_moves=1):
        self.num_of_games = self.num_of_games + 1
        if twin:
            self.twins = self.twins+1
        else:
            self.no_twins = self.no_twins + 1
        self.moves = self.moves + moves
        self.max_moves = max_moves


    def __repr__(self):
        return f"\nLiczba rozegranych gier: {self.num_of_games}\nUłożono ciasne bliźniaki: {round(self.twins/self.num_of_games, 4)*100}%\nNie ułożono ciasnych bliźniaków: {round(self.no_twins/self.num_of_games, 4)*100}%\nŚrednia liczba ruchów w grze: {round(self.moves/self.num_of_games, 2)}/{self.max_moves}"