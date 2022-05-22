import copy
import Strategy
from collections import Counter
import time


class CiasneBlizniakiGame:
    """ Gra w ciasne bliźniaki"""

    def __init__(self, mode):
        self.alphabet = []
        self.n = 0
        self.twin = []
        self.first_game = True
        self.strategy = None
        self.verbose = True
        self.mode = mode
        self.num_of_games = 1

    def play(self):
        if self.first_game:
            self.choose_parameters()
            self.first_game = False
        for i in range(self.num_of_games):
            self.game()
        self.ask()

    def choose_parameters(self):
        n = int(input("Podaj liczbę elementów w alfabecie: "))
        self.alphabet = list(map(str, input("\nPodaj alfabet: ").strip().split()))[:n]
        self.n = int(input("Podaj maksymalną liczbę ruchów: "))
        self.strategy = Strategy.Strategy(self.alphabet)
        self.strategy.strategy_place = int(input("\n1-losowy wybór miejsc\n2-wybór środkowego miejsca\nWybierz strategię wyboru miejsc: "))
        self.strategy.strategy_letter = int(input("\n1-losowy wybór liter\n2-wybór liter po kolei\nWybierz strategię wyboru liter: "))
        if self.mode != 'demo':
            self.num_of_games = int(input("Wybierz liczbę rozgrywanych gier: "))

    def game(self):
        twin_list = []
        letter = self.strategy.choose_letter(twin_list)
        twin_list.append(letter)
        for i in range(self.n - 1):
            if self.verbose:
                print("\nWybrana pozycja: ", end='')
            pos = self.strategy.choose_place(twin_list) #
            twin_list.insert(pos, " ")
            if self.verbose:
                print(twin_list)
                print("Wybrana litera: ", end='')
            letter = self.strategy.choose_letter(twin_list) #
            twin_list[pos] = letter
            if self.verbose:
                print(letter)
            is_twin = self.search_for_twins(twin_list, pos)
            if is_twin:
                if self.verbose:
                    print("Ułożono ciasne bliźniaki", self.twin)
                return
        if self.verbose:
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

    def potential_twin(self, x):
        y = copy.deepcopy(x)
        end = len(y) // 2
        start = 1
        blizniak = [0] * (len(y) // 2)
        blizniak_list = []
        while start <= len(y) // 2:
            if y[0] not in y[start:end]:
                break
            left_end = y.index(y[0], start, end)
            for i in range(left_end):
                blizniak[i] = y[i]
            start = start + left_end
            blizniak_list.append(blizniak)
            blizniak = [0] * (len(y) // 2)
        y.reverse()
        start = 1
        while start <= len(y) // 2:
            if y[0] not in y[start:end]:
                break
            right_end = y.index(y[0], start, end)
            for b in blizniak_list:
                for i in range(right_end):
                    b[-i - 1] = y[i]
            start = start + right_end
            blizniak = [0] * (len(y) // 2)
        res_list = list(map(lambda x: Counter(x).get(0), blizniak_list))
        if None in res_list:
            a = res_list.index(None)
            return [blizniak_list[a], a]
        min_zero_value = min(res_list)
        a = res_list.index(min_zero_value)
        if min_zero_value == 1:
            letter_counter = Counter(y) - Counter(blizniak_list[a] * 2)
            letter = list(letter_counter.keys())[0]
            blizniak_list[a][blizniak_list[a].index(0)] = letter
            return [blizniak_list[a], a]
        return [0, 0]

    def is_twin(self, x):
        y = copy.deepcopy(x)
        if sum(list(map(lambda x: x % 2, list(Counter(y).values())))):
            return False
        c = list(map(lambda x: x // 2, list(Counter(y).values())))
        [pot_twin, twin_num] = [0, 0]
        if max(c) != 1:
            [pot_twin, twin_num] = self.potential_twin(x)
        list1 = []
        list2 = []
        counter_list_1 = 0
        counter_list_2 = 0
        for el in y:
            ind = list(Counter(y).keys()).index(el)
            if pot_twin != 0:
                if el == pot_twin[counter_list_1] and counter_list_1 == 0 and twin_num != 0 and c[ind] != 0:
                    list1.append(el)
                    counter_list_1 = counter_list_1 + 1
                    c[ind] = c[ind] - 1
                    twin_num = twin_num - 1
                elif el == pot_twin[counter_list_1] and c[ind] != 0:
                    list1.append(el)
                    if len(list1) != len(pot_twin):
                        counter_list_1 = counter_list_1 + 1
                    c[ind] = c[ind] - 1
                else:  # elif el == pot_twin[counter_list_2]:
                    list2.append(el)
                    counter_list_2 = counter_list_2 + 1
            # stara część algorytmu
            elif c[ind] != 0:
                c[ind] = c[ind] - 1
                list1.append(el)
            else:
                list2.append(el)
        return list1 == list2 and len(list1) == len(list2)


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

