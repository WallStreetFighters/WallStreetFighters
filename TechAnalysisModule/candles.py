"""Dane wejściowe do każdej funkcji to 4 tablice jednakowej długości przechowujące
kursy open, low, high, close. Parament trend oznacza to, w jakim trendzie się znajdujemy,
(rosnący lub malejący). Roboczo przekazuję jako string, ale to kwestia gustu.
"""

LONG_BODY=0,03  #parametr określający jaką różnicę mięczy O a C traktujemy jako dużą (3%)
SHORT_BODY=0,005    #parametr określający jaką różnicę mięczy O a C traktujemy jako małą (0,5%)

def findCandleFormations(O,H,L,C,trend):
    """Znajduje na danym wykresie wszystkie możliwe fomacje świecowe i 
    zwraca je w postaci tablicy krotek ('nazwa',indeks rozpoczęcia,indeks zakończenia)"""
    #pierwsze co to rozpoznanie trendu w jakim jesteśmy!
    pass

def findDarkCloud(O,H,L,C):
    """Znajduje formację zasłony ciemnej chmury - 2-dniowa formacja odwrócenia trendu wzrostowego"""
    pass

def findPiercing(O,H,L,C):
    """Znajduje formację przenikania - 2-dniowa formacja odwrócenia trendu spadkowego"""
    pass

def findEveningStar(O,H,L,C):
    """Znajduje formację gwiazdy wieczornej - 3-dniowa formacja odwrócenia trendu wzrostowego"""
    pass

def findMorningStar(O,H,L,C):
    """Znajduje formację gwiazdy porannej - 3-dniowa formacja odwrócenia trendu spadkowego"""
    pass

def findBull3(O,H,L,C):
    """Znajduje formację trójki hossy - 5-dniowa formacja kontynuacji trendu wzrostowego"""
    pass

def findBear3(O,H,L,C):
    """Znajduje formację trójki bessy - 5-dniowa formacja kontynuacji trendu spadkowego"""
    pass

def findIsland(O,H,L,C,trend):
    """Znajduje formację wyspy. Jest to kilkudniowa (3-5) formacja odwrócenia trendu krótkotrwałego"""
    pass

def findGaps(O,H,L,C,trend):
    """Znajduje na danej tablicy lukę startową, ucieczki i wyczerpania. 
    Używać najlepiej po wybiciu z formacji."""
    pass

#(breakaway gaps)  (continuation gaps)  (exhaustion gaps)