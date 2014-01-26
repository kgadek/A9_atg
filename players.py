#!/usr/bin/env python
# coding=utf-8


"""
Przyklad pojedynczej rundy (runda nr 3)
=======================================

Gracz 1: ma kosci "3" oraz "4"
Gracz 2: ma kosc "1"
Gracz 3: ma kosc "6"
Gracz 4: ma kosci "2" i "2"

W tym momencie stan kosci opisywany jest przez napis "122346"

Gracz 1 rozpoczyna gre zglaszajac "111111" (poprawne, dobre zgloszenie bo 111111 <= 122346)
Gracz 2 zglasza "111112" (poprawne, dobre zgloszenie, choc gracz 2 o tym nie wiedzial)
Gracz 3 zglasza "111126" (poprawne, dobre zgloszenie, choc gracz wiedzial tylko o swojej 6)
Gracz 4 zglasza "111226" (poprawne, dobre zgloszenie)
Gracz 1 zglasza "111266" (poprawne zgloszenie, ktore nie jest dobre)
Gracz 2 zglasza "112266" (poprawne zgloszenie, ktore nie jest dobre)
Gracz 3 sprawdza: Gracz 2 przegrywa runde a gracz 3 wygrywa
"""
import functools
import operator
import itertools
import random
import time


def str_to_list(s):
    return [int(x) for x in s]


def list_to_str(xs):
    return ''.join(str(x) for x in xs)


def product(it):
    """ Iloczyn iteratora. """
    return reduce(operator.mul, it, 1)


def binomial(n, k):
    """ Dwumian Newtona. """
    return product(xrange(n, n - k, -1)) / product(xrange(1, k + 1))


def placements(n, it):
    """ Ilość ustawień
    """
    res = 1
    for k in it:
        res *= binomial(n, k)
        n -= k
    return res


def iterlen(it):
    """
    Długość iteratora.
    """
    return sum(1 for _ in it)


def events_a(numbs):
    """
    Zwraca ilość możliwości wypadnięcia co najmniej podanych kości _w kolejności_.

    Przestrzeń zdarzeń: 6 ** len(numbs).

    Przykład: dla numbs=[2,5] oblicza ilość zdarzeń sprzyjających gdy K1 >= 2 oraz K2 >= 5.
    """
    numbs = list(numbs)
    n = len(numbs)
    good = 6 ** n
    prev = 1

    for pos, k in enumerate(numbs, start=1):
        good -= prev * (k-1) * (6**(n-pos))
        prev *= 7 - k
    return good


def is_result_ok(results, requirements):
    """ Czy zgłoszenie jest dobre dla danego wyniku rzutu. """
    results = sorted(results)  # sort + shallow copy
    for res, req in zip(results, requirements):
        if res < req:
            return False
    return True


def probability(requirement, mydices, trials=1000):
    requirement, mydices = list(requirement), list(mydices)

    posreq = 0
    try:
        for mydice in reversed(mydices):
            while True:
                posreq -= 1
                if requirement[posreq] <= mydice:
                    break
            requirement[posreq] = 0
    except IndexError:
        return 0.0

    requirement = [req for req in requirement if req >= 2]
    if not requirement:
        return 1.0

    num_dices = len(requirement)
    ok = 0
    for _ in range(trials):
        ok += is_result_ok((random.randint(1, 6) for _ in range(num_dices)),
                           requirement)
    return float(ok) / trials


def cmp(xs, ys):
    for x, y in zip(xs, ys):
        if x < y:
            return -1
        if x > y:
            return 1
    return 0


def is_possible_such_move(prev, prop):
    return all(x <= y for x, y in zip(prev, prop)) and any(x < y for x, y in zip(prev, prop))


def showreturn(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        print "<<<<<  ", res
        return res
    return wrapper


# print time.time()
# def tmp(sx, sy): return is_possible_such_move(str_to_list(sx), str_to_list(sy))
assert not is_possible_such_move([1,1,1,6], [1,1,1,1])
assert is_possible_such_move([1,1,1,1], [1,1,1,6])
assert not is_possible_such_move([1,1,1,5], [1,1,1,5])

# noinspection PyMethodMayBeStatic,PyPep8Naming
class Player:
    def __init__(self):
        self.id = None
        self.mydices = []
        self.numofdices = 4

    def setName(self, i):
        """
        metoda wywolywana na poczatku gry, jako parametr gracz otrzymuje swoj numer (1, 2, 3, lub 4)
        """
        self.id = i

    def start(self, dice):
        """
        metoda wywolywana na poczatku rundy; parametr dice to lista z wartosciami kosci gracza
        """
        self.mydices = dice

    @showreturn
    def play(self, history):
        """
        metoda wywolywana w momencie, gdy nastepuje kolej gracza, zeby zagrac. Parametr history zawiera liste wszystkich
        dotychczasowych zgloszen wraz z numerami graczy, ktorzy ich dokonali (najnizszy indeks ma najnowsze zgloszenie;
        czyli dla gracza 4 w powyzszym przykladzie wygladalaby tak: [[3,"111126"],[2,"111112"],[1,"111111"]]). Funkcja
        powinna zwrocic lancuch opisujacy zgloszenie gracza lub slowo "CHECK" zeby sprawdzic
        """

        print ">>>>> PLAY #", self.id, " // imma got", self.mydices
        # SZCZERZE WIERZĘ, że nikt nie ma aż tak mądrego bota, by to skutecznie wykorzystać przeciwko mnie ;)
        allofmyhand = ([1]*(self.numofdices-len(self.mydices)) + self.mydices)

        if not history:
            print "return from not history"
            return list_to_str(allofmyhand)
        [_, prevdecl] = history[0]
        prevdecl = str_to_list(prevdecl)
        prob = probability(prevdecl, self.mydices)

        sigma = 0.15
        if prob < 0.5 - sigma:
            print "return from probability A"
            return "CHECK"
        elif (prob < 0.5 + sigma) and (random.random() < ((prob - 0.5 - sigma) / (2 * sigma))):
            print "return from probability B"
            return "CHECK"
        elif is_possible_such_move(prevdecl, allofmyhand):
            print "return from ALLOFMYHAND (got %s, will do %s, because %s)" % (prevdecl, allofmyhand, is_possible_such_move(prevdecl, allofmyhand))
            return list_to_str(allofmyhand)
        else:
            def props_generator():
                for digit in range(len(prevdecl)):
                    propdecl = prevdecl[:]
                    for i in range(6, 0, -1):
                        propdecl[digit] = i
                        propdecl_sorted = sorted(propdecl)
                        if is_possible_such_move(prevdecl, propdecl_sorted):
                            prob = probability(propdecl_sorted, self.mydices)
                            print "proposition: ", propdecl, "maybe:", prob, "in spite of:", prevdecl
                            yield propdecl_sorted
                        else:
                            print "proposition: ---- ", propdecl, "not possible in spite of:", prevdecl

            try:
                picked = max(props_generator(), key=lambda x: probability(x, self.mydices))
            except ValueError:
                return "CHECK"

            return list_to_str(picked)


    def result(self, points, dices, history):
        """
        funkcja wywolywana po zakonczeniu rundy; parametr points jest 4 elementowa lista, z iloscia punktow dla
        kolejnych graczy (0, 1, lub -1), parametr dices jest 4 elementowa lista zawierajaca napisy, opisujace kosci
        kolejnych graczy (od 1 do 4, kazdy napis jest posortowany w kolejnosci niemalejacej kosci; po rundzie 3 z
        przykladu powyzej parametr dices mialby wartosc ["34","1","6","22"])
        """
        self.numofdices += 1



# a = Player()
# a.setName(1)
# a.numofdices = 6
# a.start([3, 4])
#
# b = Player()
# b.setName(2)
# b.numofdices = 6
# b.start([1])
#
# c = Player()
# c.setName(3)
# c.numofdices = 6
# c.start([6])
#
# d = Player()
# d.setName(4)
# d.numofdices = 6
# d.start([2, 2])
#
# print "_____\n\n\n"
# history = []
# for player in itertools.cycle([a, b, c, d]):
#     print "ROUND"
#     history = [[player.id, player.play(history)]] + history
#     print "MOVE", player.id, ">>", history[0][1]
#     if history[0][1] == "CHECK":
#         break
