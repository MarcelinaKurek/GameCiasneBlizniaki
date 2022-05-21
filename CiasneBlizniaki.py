import copy
from Strategy import Strategy
from collections import Counter
import time


class CiasneBlizniakiGame:
    """ Gra w ciasne bliźniaki"""

    def __init__(self):
        self.alphabet = []
        self.n = 0
        self.twin = []
        self.first_game = True
        self.strategy = None

    def play(self):
        if self.first_game:
            self.choose_parameters()
            self.first_game = False
        self.game()
        self.ask()

    def choose_parameters(self):
        n = int(input("Podaj liczbę elementów w alfabecie: "))
        self.alphabet = list(map(str, input("\nPodaj alfabet: ").strip().split()))[:n]
        self.n = int(input("Podaj maksymalną liczbę ruchów: "))
        self.strategy = Strategy(self.alphabet)
        self.strategy.strategy_place = int(input("\n1-losowy wybór miejsc\n2-wybór środkowego miejsca\nWybierz strategię wyboru miejsc: "))
        self.strategy.strategy_letter = int(input("\n1-losowy wybór liter\n2-wybór liter po kolei\nWybierz strategię wyboru liter: "))

    def game(self):
        twin_list = []
        letter = self.strategy.choose_letter(twin_list) #
        twin_list.append(letter)
        for i in range(self.n - 1):
            print("\nWybrana pozycja: ", end='')
            pos = self.strategy.choose_place(twin_list) #
            twin_list.insert(pos, " ")
            print(twin_list)
            print("Wybrana litera: ", end='')
            letter = self.strategy.choose_letter(twin_list) #
            twin_list[pos] = letter
            print(letter)
            is_twin = self.search_for_twins(twin_list, pos)
            if is_twin:
                print("Ułożono ciasne bliźniaki", self.twin)
                return
        print("Nie ułożono ciasnych bliźniaków")
        return

    def ask(self):
        print("\nCzy chcesz zagrać ponownie? (y/n)?")
        ans = input()
        if ans == 'y':
            print("\nCzy chcesz zmienić parametry gry? (y/n)?")
            ans = input()
            if ans == 'y':
                self.choose_parameters()
            self.strategy.places = 1
            self.play()
        else:
            return

    def is_twin(self, x):
        y = copy.deepcopy(x)
        if sum(list(map(lambda x: x % 2, list(Counter(y).values())))):
            return False
        c = list(map(lambda x: x // 2, list(Counter(y).values())))
        list1 = []
        list2 = []
        for el in y:
            ind = list(Counter(y).keys()).index(el)
            if c[ind] != 0:
                c[ind] = c[ind] - 1
                list1.append(el)
            else:
                list2.append(el)
        return list1 == list2


    def search_for_twins(self, l, key):
        a = 1
        while (a <= len(l)):
            if (key - a >= 0 and key + a <= len(l)):
                first = key - a
                last = key
            else:
                first = 0
                last = a
            sublist = l[first:last + 1]
            if (self.is_twin(sublist)):
                self.twin = sublist
                return True

            for i in range(len(sublist) - 1):
                first = first + 1
                last = last + 1
                if last + 1 > len(l):
                    break
                sublist = l[first:last + 1]
                if (self.is_twin(sublist)):
                    self.twin = sublist
                    return True
            a = a + 2
        return False

