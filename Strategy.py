import random
import CiasneBlizniaki

class Strategy:

    def __init__(self, alphabet, strategy_place=None, strategy_letter=None):
        self.strategy_place = strategy_place
        self.strategy_letter = strategy_letter
        self.alphabet = alphabet
        self.places = 1
        self.chosen_letters = 0

    def choose_place(self, twin_list):
        gra = CiasneBlizniaki.CiasneBlizniakiGame()
        place = 0
        if self.strategy_place == 1: #losowy wybór miejsca z rozkładu jednostajnego
            place = random.randint(0, self.places)
        elif self.strategy_place == 2: #wybór środkowego miejsca
            place = self.places // 2 +1
        elif self.strategy_place == 3: #wybór zawsze tego samego miejsca
            place = 1
        elif self.strategy_place == 4: #wybór miejsca zmniejszajacego alfabet o 2 litery
            if twin_list[2] == twin_list[0] or twin_list[2]==twin_list[1]:
                place = 3
            else:
                place = 2
        elif self.strategy_place == 5: #wybieramy losowo spośród miejsc w które można wpisać najmniej liter nie tworząc ciasnego bliźniaka
            n = len(twin_list)
            n_l = [] #tablica gdzie wpisujemy pod indeksem i liczbę liters, których nie można wpisać w i-tą lukę
            max_index = [] #tu wpisujemy indeksy z dla których wartość n_l[i] jest równa max(n_l)
            for i in range(n+1):
                a = 0 #liczba liter, które może wpisać 2 gracz nie przegrywając gry
                for j in self.alphabet:
                    twin_list[i] = j
                    is_twin = gra.search_for_twins(twin_list, i)
                    if is_twin:
                        a = a + 1
                n_l.append(a)
            for i in range(n+1):
                if n_l[i] == max(n_l):
                    max_index.append(i)
            place = random.choice(max_index)
        self.places = self.places+1
        return place

    def choose_letter(self, twin_list, luka):
        pos = 0
        gra = CiasneBlizniaki.CiasneBlizniakiGame()
        if self.strategy_letter == 1: #losowy wybór litery
            pos = random.randint(0, len(self.alphabet)-1)
        elif self.strategy_letter == 2: #wybór liter po kolei
            pos = self.chosen_letters % len(self.alphabet)
            self.chosen_letters = self.chosen_letters + 1
        elif self.strategy_letter == 3: #wybór litery alfabetycznie z tych co można wstawić (tzn. gdy mogę to zawsze wstawiam A, jeżeli nie to B itd.)
            for y in self.alphabet:
                twin_list[luka] = y
                is_twin = gra.search_for_twins(twin_list, luka)
                if not is_twin:
                    pos = y
                    break
        elif self.strategy_letter == 4: #wybór litery losowej spośród tych co można wstawić
            for y in self.alphabet:
                twin_list[luka] = y
                alter_alph = [] #tu wpisujemy litery, które można wstawić
                is_twin = gra.search_for_twins(twin_list, luka)
                if not is_twin:
                    alter_alph.append(y)
            pos = random.choice(alter_alph)
        letter = self.alphabet[pos]
        return letter
