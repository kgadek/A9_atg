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
import random


def str_to_list(s):
    """
    @type s: str
    :rtype: list[int]

    >>> str_to_list("11233345")
    [1, 1, 2, 3, 3, 3, 4, 5]
    """
    return [int(x) for x in s]


def list_to_str(xs):
    """
    @type xs: list[int]
    :rtype: str

    >>> list_to_str([1,1,1,2,2,3,5,6])
    '11122356'
    """
    return ''.join(str(x) for x in xs)


def is_result_ok(results, requirements):
    """ Czy zgłoszenie jest dobre dla danego wyniku rzutu?
    is_result
    @param results: list[int]
    @param requirements: list[int]
    :rtype: bool

    >>> is_result_ok([1,1,1,2],[1,1,1,1])
    True
    >>> is_result_ok([1,1,1,2],[1,1,1,2])
    True
    >>> is_result_ok([1,1,1,2],[1,1,1,3])
    False
    >>> is_result_ok([1,2,2,3,4,6], [1,1,1,1,1,1])
    True
    >>> is_result_ok([1,2,2,3,4,6], [1,1,1,1,1,2])
    True
    >>> is_result_ok([1,2,2,3,4,6], [1,1,1,1,2,6])
    True
    >>> is_result_ok([1,2,2,3,4,6], [1,1,1,2,2,6])
    True
    >>> is_result_ok([1,2,2,3,4,6], [1,1,1,2,6,6])
    False
    >>> is_result_ok([1,2,2,3,4,6], [1,1,2,2,6,6])
    False
    >>>
    """
    results = sorted(results)  # sort + shallow copy
    for res, req in zip(results, requirements):
        if res < req:
            return False
    return True


def probability(requirement, mydices, trials=1000):
    """ Zwraca p-stwo zgłoszenia mając na uwadze posiadane kości.
    @param requirement: list[int]
    @param mydices: list[int]
    @param trials: int
    :rtype: float

    >>> probability([1,1,1], [2])
    1.0
    >>> probability([6,6,6], [6,6,6])
    1.0
    >>> 5./6-0.1 < probability([1,2,6], [6]) < 5./6+0.1
    True
    """

    requirement, mydices = list(requirement), list(mydices)

    # Z puli wymagań "ściągamy" to, co posiadamy (tj. to, co na pewno już jest).
    posreq = 0
    try:
        for mydice in reversed(mydices):
            while True:
                posreq -= 1
                if requirement[posreq] <= mydice:
                    break
            requirement[posreq] = 0
    except IndexError:  # ...jeśli wymaganie jest zbyt mocne na obecną rękę
        return 0.0
    requirement = [req for req in requirement if req >= 2]
    if not requirement:  # ...jeśli wymaganie będzie na pewno spełnione
        return 1.0

    # obliczanie p-stwa metodą monte-carlo
    num_dices = len(requirement)
    ok = 0
    for _ in range(trials):
        ok += is_result_ok((random.randint(1, 6) for _ in range(num_dices)),
                           requirement)
    return float(ok) / trials


def is_possible_such_move(prev, prop):
    """ Czy podane zgłoszenie jest dopuszczalne wg zasad w kontekście zgłoszenia poprzedniego gracza?

    // Roznica w stosunku do wersji 1: Zgloszenia musza byc "starsze" wg definicji "kazdy znak w zgloszeniu wiekszy lub
    rowny temu w zgloszeniu poprzednim, przynajmniej jeden znak scisle wiekszy". Ta wersja sedziego przekazuje tez
    historie gry w trzecim parametrze funkcji result.

    @param prev: list[int]
    @param prop: list[int]
    :rtype: bool

    >>> is_possible_such_move([1,1,1,1,1,1], [1,1,1,1,1,2])
    True
    >>> is_possible_such_move([1,1,1,1,1,2], [1,1,1,1,2,6])
    True
    >>> is_possible_such_move([1,1,1,1,2,6], [1,1,1,1,2,2])
    False
    >>> is_possible_such_move([1,1,1,1,2,6], [1,1,1,1,3,5])
    False
    >>> is_possible_such_move([1,1,1,1,2,6], [1,1,1,2,2,6])
    True
    >>> is_possible_such_move([1,1,1,2,2,6], [1,1,2,2,6,6])
    True
    """
    return all(x <= y for x, y in zip(prev, prop)) and any(x < y for x, y in zip(prev, prop))


class Player:
    def __init__(self):
        self.id = None
        self.mydices = []
        self.numofdices = 4

    # noinspection PyPep8Naming
    def setName(self, i):
        """ Metoda wywolywana na poczatku gry, jako parametr gracz otrzymuje swoj numer (1, 2, 3, lub 4).
        @param i: int
        """
        self.id = i

    def start(self, dice):
        """ Metoda wywolywana na poczatku rundy; parametr dice to lista z wartosciami kosci gracza.
        @param dice: list[int]
        """
        self.mydices = [int(x) for x in dice]

    def play(self, history):
        """
        metoda wywolywana w momencie, gdy nastepuje kolej gracza, zeby zagrac. Parametr history zawiera liste wszystkich
        dotychczasowych zgloszen wraz z numerami graczy, ktorzy ich dokonali (najnizszy indeks ma najnowsze zgloszenie;
        czyli dla gracza 4 w powyzszym przykladzie wygladalaby tak: [[3,"111126"],[2,"111112"],[1,"111111"]]). Funkcja
        powinna zwrocic lancuch opisujacy zgloszenie gracza lub slowo "CHECK" zeby sprawdzic.

        @param history: list[list[int | str]]
        :rtype: str
        """

        # SZCZERZE WIERZĘ, że nikt nie ma aż tak mądrego bota, by to skutecznie wykorzystać przeciwko mnie ;)
        allofmyhand = ([1]*(self.numofdices-len(self.mydices)) + self.mydices)

        # Jeśli zaczynamy to startujemy z maksymalnym "pewniakiem"
        if not history:
            return list_to_str(allofmyhand)

        # Decyzja jedynie na podstawie poprzedniego ruchu.
        [_, prevdecl] = history[0]
        prevdecl = str_to_list(prevdecl)
        prob = probability(prevdecl, self.mydices)

        sigma = 0.3
        if prob < 0.5 - sigma:
            # zbyt niskie p-stwo, sprawdzamy
            return "CHECK"
        elif (prob < 0.5 + sigma) and (random.random() < ((prob - 0.5 - sigma) / (2 * sigma))):
            # p-stwo w granicach rozsądku, ale (losowa) decyzja by jednak sprawdzić
            return "CHECK"
        elif is_possible_such_move(prevdecl, allofmyhand):
            # jeśli możemy przebić pewniakiem to tak robimy
            return list_to_str(allofmyhand)
        else:
            def prop_ctx(x):
                return probability(x, self.mydices)

            def props_generator():  # generator propozycji przebicia
                for digit in range(len(prevdecl)):  # zmieniamy tylko jedną cyfrę
                    propdecl = prevdecl[:]          # (shallow copy)
                    for i in range(6, 0, -1):
                        propdecl[digit] = i
                        propdecl_sorted = sorted(propdecl)
                        if is_possible_such_move(prevdecl, propdecl_sorted):
                            yield propdecl_sorted

            try:  # wybieramy najbardziej prawdopodobną propozycję
                picked = max(props_generator(), key=prop_ctx)
            except ValueError:  # jeśli nie ma żadnej pasującej propozycji to po prostu sprawdzamy
                return "CHECK"

            return list_to_str(picked)

    def result(self, points, dices, history):
        """
        funkcja wywolywana po zakonczeniu rundy; parametr points jest 4 elementowa lista, z iloscia punktow dla
        kolejnych graczy (0, 1, lub -1), parametr dices jest 4 elementowa lista zawierajaca napisy, opisujace kosci
        kolejnych graczy (od 1 do 4, kazdy napis jest posortowany w kolejnosci niemalejacej kosci; po rundzie 3 z
        przykladu powyzej parametr dices mialby wartosc ["34","1","6","22"]).

        // Roznica w stosunku do wersji 1: Zgloszenia musza byc "starsze" wg definicji "kazdy znak w zgloszeniu wiekszy
        lub rowny temu w zgloszeniu poprzednim, przynajmniej jeden znak scisle wiekszy". Ta wersja sedziego przekazuje
        tez historie gry w trzecim parametrze funkcji result

        @param points: list[int]
        @param dices: list[str]
        @param history: list[list[int | str]]
        """
        self.numofdices += 1


# if __name__ == "__main__":
#     import doctest
#     print "tests"
#     doctest.testmod()