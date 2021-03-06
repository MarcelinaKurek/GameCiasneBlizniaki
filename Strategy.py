import random
import CiasneBlizniaki
import copy

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
            place = self.places // 2 + 1
        elif self.strategy_place == 3: #wybór zawsze tego samego miejsca
            place = 1
        elif self.strategy_place == 4: #wybór miejsca zmniejszajacego alfabet o 2 litery
            if len(twin_list) < 3:
                place = len(twin_list)
            else:
                if twin_list[2] == self.alphabet[0] or twin_list[2] == self.alphabet[1]:
                    place = 3
                else:
                    place = 2
        elif self.strategy_place == 5: #wybieramy losowo spośród miejsc w które można wpisać najmniej liter nie tworząc ciasnego bliźniaka
            twin_list1 = copy.deepcopy(twin_list)
            n = len(twin_list)
            n_l = [] #tablica gdzie wpisujemy pod indeksem i liczbę liters, których nie można wpisać w i-tą lukę
            max_index = [] #tu wpisujemy indeksy z dla których wartość n_l[i] jest równa max(n_l)
            for i in range(n+1):
                if i == 0:
                    twin_list1.insert(0, '')
                elif i == 1:
                    twin_list1 = twin_list1[1:]
                if i == n:
                    twin_list1.append('')
                a = 0 #liczba liter, które może wpisać 2 gracz nie przegrywając gry
                for j in self.alphabet:
                    twin_list1[i] = j
                    is_twin = gra.search_for_twins(twin_list1, i)
                    #print(twin_list1, i, j)
                    if is_twin:
                        a = a + 1
                n_l.append(a)
            #print("nl", n_l)
            for i in range(n+1):
                if n_l[i] == max(n_l):
                    max_index.append(i)
                    #print(n_l, max_index, 'max index')
            place = random.choice(max_index)
        self.places = self.places+1
        return place

    def choose_letter(self, twin_list, luka=0):
        pos = 0
        gra = CiasneBlizniaki.CiasneBlizniakiGame()
        if self.strategy_letter == 1: #losowy wybór litery
            pos = random.randint(0, len(self.alphabet)-1)
            letter = self.alphabet[pos]
        elif self.strategy_letter == 2: #wybór liter po kolei
            pos = self.chosen_letters % len(self.alphabet)
            self.chosen_letters = self.chosen_letters + 1
            letter = self.alphabet[pos]
        elif self.strategy_letter == 3: #wybór litery alfabetycznie z tych co można wstawić (tzn. gdy mogę to zawsze wstawiam A, jeżeli nie to B itd.)
            for y in self.alphabet:
                if len(twin_list) !=0:
                    twin_list[luka] = y
                    is_twin = gra.search_for_twins(twin_list, luka)
                    #print(twin_list, luka, is_twin)
                    if not is_twin:
                        letter = y
                        return letter
                else:
                    letter = self.alphabet[0]
            letter = self.alphabet[0]
        elif self.strategy_letter == 4: #wybór litery losowej spośród tych co można wstawić
            alter_alph = []  # tu wpisujemy litery, które można wstawić
            for y in self.alphabet:
                if len(twin_list) != 0:
                    twin_list[luka] = y
                    is_twin = gra.search_for_twins(twin_list, luka)
                    if not is_twin:
                        alter_alph.append(y)
            if len(twin_list) ==0 or len(alter_alph) ==0:
                letter = random.choice(self.alphabet)
            else:
                letter = random.choice(alter_alph)

        return letter
