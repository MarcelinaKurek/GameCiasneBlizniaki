import copy
import Strategy
from collections import Counter
from BNode import BNode
import time
import treelib


class CiasneBlizniakiGame:
    """ Gra w ciasne bliźniaki"""

    def __init__(self):
        self.alphabet = []
        self.n = 0
        self.twin = []
        self.first_game = True
        self.strategy = None
        self.verbose = True
        self.mode = ""
        self.num_of_games = 1

    def play(self):
        if self.first_game:
            self.choose_parameters()
            self.first_game = False
        for i in range(self.num_of_games):
            self.game()
            self.ask('y', 'n')
        self.ask()


    def choose_parameters(self):
        tryb = int(input("Wybierz tryb gry: 1-demo, 2-gra"))
        n = int(input("Podaj liczbę elementów w alfabecie: "))
        self.alphabet = list(map(str, input("\nPodaj alfabet: ").strip().split()))[:n]
        self.n = int(input("Podaj maksymalną liczbę ruchów: "))
        self.strategy = Strategy.Strategy(self.alphabet)
        self.strategy.strategy_place = int(input("\n1-losowy wybór miejsc\n2-wybór środkowego miejsca\nWybierz strategię wyboru miejsc: "))
        self.strategy.strategy_letter = int(input("\n1-losowy wybór liter\n2-wybór liter po kolei\nWybierz strategię wyboru liter: "))
        if tryb == 1:
            self.mode = 'demo'
        if tryb ==2:
            self.mode = 'gra'
            self.verbose = False
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

    def ask(self, ans='', ans2=''):
        if ans != '':
            print("\nCzy chcesz zagrać ponownie? (y/n)?")
            ans = input()
        if ans == 'y':
            if ans2 !='':
                print("\nCzy chcesz zmienić parametry gry? (y/n)?")
                ans2 = input()
            if ans2 == 'y':
                self.choose_parameters()
            self.strategy.places = 1
            self.play()
        else:
            return

    def is_simple_twin(self, x, return_twin=False):
        """
        Funkcja zwaraca wartość true, jeśli da się rozdzielić bliźniaka na
        2 listy zachwoując kolejność elementów
        :param x:
        :param return_twin:
        :return:
        """
        y = copy.deepcopy(x)
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
        if return_twin:
            return list1
        return list1 == list2

    def potential_twin(self, x):
        """
        :param x:
        :return: fragment ciasnego bliźniaka, którego jesteśm pewni na podstawie
        początku i końca listy
        """
        y = copy.deepcopy(x)
        end = len(y) // 2
        start = 1
        blizniak = [0] * (len(y) // 2)
        if y[0] in y[start:end]:
            left_end = y.index(y[0], start, end)
            for i in range(left_end):
                blizniak[i] = y[i]
        y.reverse()
        start = 1
        if y[0] in y[start:end]:
            right_end = y.index(y[0], start, end)
            for i in range(right_end):
                blizniak[-i - 1] = y[i]
        return blizniak

    def split_for_twins(self, x, twin_structure=False):
        """
        Funkcja rodziela ciasne bliźniaki według zadanej struktury
        :param x:
        :param twin_structure:
        :return:
        """
        y = copy.deepcopy(x)
        c = list(map(lambda x: x // 2, list(Counter(y).values())))
        list1 = []
        list2 = []
        counter_list_1 = 0
        counter_list_2 = 0
        for el in y:
            ind = list(Counter(y).keys()).index(el)
            if twin_structure:
                if el == twin_structure[counter_list_1] and counter_list_1 == 0 and c[ind] != 0:
                    list1.append(el)
                    counter_list_1 = counter_list_1 + 1
                    c[ind] = c[ind] - 1
                elif el == twin_structure[counter_list_1] and c[ind] != 0:
                    list1.append(el)
                    if len(list1) != len(twin_structure):
                        counter_list_1 = counter_list_1 + 1
                    c[ind] = c[ind] - 1
                else:
                    list2.append(el)
                    counter_list_2 = counter_list_2 + 1
        return list1 == list2 and len(list1) == len(list2)

    def tree_check(self, x, assured_twin):
        counter_rest = Counter(x) - Counter(assured_twin * 2)
        if sum(counter_rest.values()) != list(Counter(assured_twin).values())[
            list(Counter(assured_twin).keys()).index(0)]:
            return False
        start = assured_twin.index(0)  # osobny przypadek dla pewnych bliźniaków
        assured_twin.reverse()
        letters_len = sum(list(counter_rest.values()))  # //2
        stop = len(x) - assured_twin.index(0)
        assured_twin.reverse()
        l_counted = self.count_elements(x)
        counter_nones = Counter(x[start:stop]) - counter_rest  # Counter nadmiarowych liter, których brakuje nam w strukturze ciasnego bliźniaka
        counter_values = list(counter_rest.keys())
        is_in_counter = list(map(lambda x: x in counter_values, list(counter_nones.keys())))
        max_nones = 0
        for i in range(len(list(counter_nones.values()))):
            if is_in_counter[i]:
                max_nones = max_nones + list(counter_nones.values())[i]
        btree = treelib.Tree()
        btree.create_node(1, 1, data=BNode(0, 0))
        a = 0
        ind = 2
        sure = False
        for i in range(start, stop):
            if x[i] in counter_rest.keys():
                if l_counted[i] == 1:
                    sure = True
                for j in range(2 ** a):
                    d = btree.depth()
                    if btree.get_node(ind // 2) is not None:
                        parent_letters = btree.get_node(ind // 2).data.letters_in_path
                        parent_nones = btree.get_node(ind // 2).data.nones_in_path
                        is_full = self.check_letters(ind // 2, x[i], btree, counter_rest)
                        if parent_letters < letters_len and not is_full:
                            btree.create_node(ind, ind, parent=ind // 2,
                                              data=BNode(x[i], l_counted[i], parent_letters + 1, parent_nones))
                        if not sure and parent_nones < max_nones:
                            btree.create_node(ind + 1, ind + 1, parent=ind // 2,
                                              data=BNode(0, 0, parent_letters, parent_nones + 1))
                    ind = ind + 2
                a = a + 1
                sure = False

        for inds in btree.paths_to_leaves():
            list_of_nodes = []
            for i in range(1, len(inds)):
                node = btree.get_node(inds[i]).data.letter
                if node != 0:
                    list_of_nodes.append(node)
            if self.is_simple_twin(list_of_nodes):
                twin = self.is_simple_twin(list_of_nodes, True)
                print(twin)
                for j in range(len(twin)):
                    print(assured_twin)
                    ind = assured_twin.index(0)
                    assured_twin[ind] = twin[j]
                return assured_twin
            else:
                p_twin = self.potential_twin(list_of_nodes)
                if 0 not in p_twin:
                    t = self.split_for_twins(list_of_nodes, p_twin)
                    if t:
                        for j in range(len(p_twin)):
                            ind = assured_twin.index(0)
                            assured_twin[ind] = p_twin[j]
                        return assured_twin
        return False

    def check_letters(self, num, letter, btree, counter_rest):
        node_letters = []
        node_letters.append(letter)
        for node in btree.rsearch(num):
            if btree[node].data.letter != 0:
                node_letters.append(btree[node].data.letter)
        equal = Counter(node_letters) == counter_rest
        too_many_elements = len((Counter(node_letters) - counter_rest).keys()) != 0
        return too_many_elements and not equal

    def count_elements(self, l):
        counter_list = []
        for i in range(len(l)):
            counted = l[0:i].count(l[i]) + 1
            counter_list.append(counted)
        return counter_list

    def is_twin(self, x):
        y = copy.deepcopy(x)
        if sum(list(map(lambda x: x % 2, list(Counter(y).values())))):
            return False
        if self.is_simple_twin(y):
            return True
        p_twin = self.potential_twin(y)
        if 0 not in p_twin:
            return self.split_for_twins(y, p_twin)
        twin_inside = self.tree_check(y, p_twin)
        if twin_inside != False:
            return self.split_for_twins(y, twin_inside)
        return False


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

