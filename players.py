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
import operator
import itertools


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



# noinspection PyMethodMayBeStatic,PyPep8Naming
class Player:
    def __init__(self):
        self.id = None

    def setName(self, i):
        """
        metoda wywolywana na poczatku gry, jako parametr gracz otrzymuje swoj numer (1, 2, 3, lub 4)
        """
        self.id = i

    def start(self, dice):
        """
        metoda wywolywana na poczatku rundy; parametr dice to lista z wartosciami kosci gracza
        """
        pass

    def play(self, history):
        """
        metoda wywolywana w momencie, gdy nastepuje kolej gracza, zeby zagrac. Parametr history zawiera liste wszystkich
        dotychczasowych zgloszen wraz z numerami graczy, ktorzy ich dokonali (najnizszy indeks ma najnowsze zgloszenie;
        czyli dla gracza 4 w powyzszym przykladzie wygladalaby tak: [[3,"111126"],[2,"111112"],[1,"111111"]]). Funkcja
        powinna zwrocic lancuch opisujacy zgloszenie gracza lub slowo "CHECK" zeby sprawdzic
        """
        pass

    def result(self, points, dices):
        """
        funkcja wywolywana po zakonczeniu rundy; parametr points jest 4 elementowa lista, z iloscia punktow dla
        kolejnych graczy (0, 1, lub -1), parametr dices jest 4 elementowa lista zawierajaca napisy, opisujace kosci
        kolejnych graczy (od 1 do 4, kazdy napis jest posortowany w kolejnosci niemalejacej kosci; po rundzie 3 z
        przykladu powyzej parametr dices mialby wartosc ["34","1","6","22"])
        """
        pass
