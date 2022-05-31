
class Statistics:

    def __init__(self):
        self.num_of_games = 0
        self.no_twins = 0
        self.twins = 0
        self.moves = 0

    def update(self, twin, moves):
        self.num_of_games = self.num_of_games + 1
        if twin:
            self.twins = self.twins+1
        else:
            self.no_twins = self.no_twins + 1
        self.moves = self.moves + moves

    def __repr__(self):
        return f"\nLiczba rozegranych gier: {self.num_of_games}\nUłożono ciasne bliźniaki: {self.twins}\nNie ułożono ciasnych bliźniaków: {self.no_twins}\nŚrednia liczba ruchów w grze: {self.moves/self.num_of_games}"