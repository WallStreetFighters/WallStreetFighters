# coding: utf-8

"""Dane wejściowe do każdej funkcji to 4 tablice jednakowej długości przechowujące
kursy open, low, high, close. Parament trend oznacza to, w jakim trendzie się znajdujemy,
(rosnący lub malejący). Zgodnie z konwencją Pawła 1=trend rosnący, -1 malejący.
"""

import trendAnalysis as trend

STRONG_TREND=0.3
STRAIGHT_TREND_VUL=0.1
LONG_BODY=0.03  #parametr określający jaką różnicę mięczy O a C traktujemy jako dużą (3%)
SHORT_BODY=0.005    #parametr określający jaką różnicę mięczy O a C traktujemy jako małą (0,5%)

def findCandleFormations(O,H,L,C,trend):
    """Szuka na wykresie formacji świecowych, dla każdej formacji która wystąpiła
    zwraca tablicę krotek ('nazwa',indeks rozpoczęcia, indeks zakończenia). Przy czym,
    dla każdej formacji jest co najwyżej jedna krotka z jej ostatnim wystąpieniem"""
    if not (len(O)==len(H)==len(L)==len(C)):
        print "Tablice są różnej długości - co to kurwa ma być?"
        return None
    result=[]
    if trend==1:
        result.append(findBull3(O,H,L,C))        
        result.append(findEveningStar(O,C))                
        result.append(findDarkCloud(O,C))
    else:
        result.append(findBear3(O,H,L,C))        
        result.append(findMorningStar(O,C))                 
        result.append(findPiercing(O,C))
    return [value for value in result if value != None]

"""Algorytm szukania każdej formacji jest identyczny: lecimy od końca i sprawdzamy po kolei
świeczki czy są takie jak formacja nakazuje. Jeśli znajdziemy coś dobrego to kończymy 
(nie interesuje nas co było wcześniej), jeśli nie to zwracamy None"""    

def findDarkCloud(O,C):
    """Znajduje formację zasłony ciemnej chmury - 2-dniowa formacja odwrócenia trendu wzrostowego"""
    if(len(O)<2):        
        return None    
    for i in range(len(O)-1, 1, -1):
        body1=(C[i-1]-O[i-1])/O[i-1]
        body2=(C[i]-O[i])/O[i]        
        if body2 > -LONG_BODY or body1 <LONG_BODY:
            continue        
        if O[i]<=C[i-1]:
            return
        body1mid=C[i-1]-(C[i-1]-O[i-1])/2
        if(C[i]>=body1mid):
            continue
        return ('dark_cloud',i-1,i)
    return None

def findPiercing(O,C):
    """Znajduje formację przenikania - 2-dniowa formacja odwrócenia trendu spadkowego"""
    if(len(O)<2):        
        return None    
    for i in range(len(O)-1, 1, -1):
        body1=(C[i-1]-O[i-1])/O[i-1]
        body2=(C[i]-O[i])/O[i]
        if body2 < LONG_BODY or body1 > -LONG_BODY:
            continue
        if O[i]>=C[i-1]:
            return
        body1mid=C[i-1]-(C[i-1]-O[i-1])/2
        if(C[i]<=body1mid):
            continue
        return ('piercing',i-1,i)
    return None    

def findEveningStar(O,C):
    """Znajduje formację gwiazdy wieczornej - 3-dniowa formacja odwrócenia trendu wzrostowego"""
    if(len(O)<3):        
        return None    
    for i in range(len(O)-1, 2, -1):
        body1=(C[i-2]-O[i-2])/O[i-2]
        body2=(C[i-1]-O[i-1])/O[i-1]
        body3=(C[i]-O[i])/O[i]
        if body1 < LONG_BODY or abs(body2) > SHORT_BODY or body3 > -LONG_BODY:
            continue
        if O[i-1]<=C[i-2] or C[i-1]<=C[i-2] or O[i]>=C[i-1]:
            continue
        body1mid=C[i-2]-(C[i-2]-O[i-2])/2
        if(C[i]>=body1mid):
            continue
        return ('evening_star',i-2,i)
    return None    

def findMorningStar(O,C):
    """Znajduje formację gwiazdy porannej - 3-dniowa formacja odwrócenia trendu spadkowego"""
    if(len(O)<3):        
        return None    
    for i in range(len(O)-1, 2, -1):
        body1=(C[i-2]-O[i-2])/O[i-2]
        body2=(C[i-1]-O[i-1])/O[i-1]
        body3=(C[i]-O[i])/O[i]
        if body1 > -LONG_BODY or abs(body2) > SHORT_BODY or body3 < LONG_BODY:
            continue
        if O[i-1]>=C[i-2] or C[i-1]>=C[i-2] or O[i]<=C[i-1]:
            continue
        body1mid=C[i-2]-(C[i-2]-O[i-2])/2
        if(C[i]<=body1mid):
            continue
        return ('morning_star',i-2,i)
    return None    

def findBull3(O,H,L,C):
    """Znajduje formację trójki hossy - 5-dniowa formacja kontynuacji trendu wzrostowego"""
    if(len(O)<5):        
        return None    
    for i in range(len(O)-1, 4, -1):
        body1=(C[i-4]-O[i-4])/O[i-4]
        body2=(C[i-3]-O[i-3])/O[i-3]
        body3=(C[i-2]-O[i-2])/O[i-2]
        body4=(C[i-1]-O[i-1])/O[i-1]
        body5=(C[i]-O[i])/O[i]
        #długości korpusów
        if (body1 < LONG_BODY or abs(body2) > SHORT_BODY or 
            abs(body2) > SHORT_BODY or abs(body2) > SHORT_BODY or body5 < LONG_BODY):
            continue
        #środek porusza się wewnątrz zakresu pierwszej świecy
        if (max(O[i-1],C[i-1])>H[i-4] or max(O[i-2],C[i-2])>H[i-4] or 
            max(O[i-3],C[i-3])>H[i-4] or
            min(O[i-1],C[i-1])<L[i-4] or min(O[i-2],C[i-2])<L[i-4] or 
            min(O[i-3],C[i-3])<L[i-4]):
            continue
        #co najmniej 2 świece w środku czarne
        falls=[x for x in [body2,body3,body4] if x<0]
        if(len(falls)<2):
            continue
        #nowe maksimum na koniec
        if(C[i]<=C[i-4]):
            continue
        return ('bull3',i-4,i)
    return None    

def findBear3(O,H,L,C):
    """Znajduje formację trójki bessy - 5-dniowa formacja kontynuacji trendu spadkowego"""
    if(len(O)<5):        
        return None    
    for i in range(len(O)-1, 4, -1):
        body1=(C[i-4]-O[i-4])/O[i-4]
        body2=(C[i-3]-O[i-3])/O[i-3]
        body3=(C[i-2]-O[i-2])/O[i-2]
        body4=(C[i-1]-O[i-1])/O[i-1]
        body5=(C[i]-O[i])/O[i]
        #długości korpusów
        if (body1 > -LONG_BODY or abs(body2) > SHORT_BODY or 
            abs(body2) > SHORT_BODY or abs(body2) > SHORT_BODY or body5 > -LONG_BODY):
            continue
        #środek porusza się wewnątrz zakresu pierwszej świecy
        if (max(O[i-1],C[i-1])>H[i-4] or max(O[i-2],C[i-2])>H[i-4] or 
            max(O[i-3],C[i-3])>H[i-4] or
            min(O[i-1],C[i-1])<L[i-4] or min(O[i-2],C[i-2])<L[i-4] or 
            min(O[i-3],C[i-3])<L[i-4]):
            continue
        #co najmniej 2 świece w środku białe
        rises=[x for x in [body2,body3,body4] if x>0]
        if(len(rises)<2):
            continue
        #nowe minimum na koniec
        if(C[i]>=C[i-4]):
            continue
        return ('bear3',i-4,i)
    return None    

"""luki traktuję jako osobną rzecz od formacji świecowych 
(podobnie zresztą jak literatura)
po pierwsze nie wymagają świec (wystarczy zwykły wykres słupkowy), 
po drugie kształtują się przez dłuższy czas, więc są IMO ważniejsze"""

def isStraightTrend(array):    
    """Sprawdzamy czy tablica opisuje zdecydowany ruch w górę lub w dół.
    Robimy to wyliczając regresję i sprawdzając czy wszystkie punkty w tablicy 
    są w pasie regresja +/- jakieś sensitivity. Oczywiście sprawdzamy też czy sam trend
    jest odpowiednio silny poprzez badanie współczynnika kierunkowego prostej."""    
    a, b = trend.regression(array)
    if abs(a) < STRONG_TREND:
        return 0
    for i in range(array.size):
            y = a*i+b
            if y > (1+STRAIGHT_TREND_VUL)*array[i] or y < (1-STRAIGHT_TREND_VUL)*array[i]:
                    return 0
    return a       

def findGaps(H,L,C):
    """Znajduje na danym wykresie (lub jego wycinku) lukę startową, ucieczki i wyczerpania. 
    Używać najlepiej na możliwie krótkim okresie, np po wybiciu z formacji. 
    Interpretacja: Luka startowa - sygnał rozpoczęcia trendu, 
    luka ucieczki - potwierdzenie siły trendu + orientacyjne określenie jego zasięgu (zazwyczaj jest w połowie)
    luka wyczerpania - sygnał że trend się wkrótce skończy    
    Uwaga na wartości zwracane przez funkcję, dostajemy None, lub parę składającą się
    ze stringa (po stringu poznamy co jest drugim argumentem) i krotki 3 lub 2 elementowej 
    lub pojedynczego elementu"""
    trend=isStraightTrend(C)
    if not (len(H)==len(L)==len(C)) or trend==0:
        return None    
    gaps=[] 
    if(trend>0):
        #szukamy wszystkich luk na wykresie (uwaga - w kolejności od najnowszej do najstarszej)
        for i in range (len(H)-1):
            if(H[i]<L[i+1]):
                #pierwszy element pary to indeks, drugi to wartość (połowa wysokości luki)
                gaps.append( (i,H[i]+(L[i+1]-H[i])/2.) )    
        for i in range(len(gaps)):
            pass
    #dla trendu malejącego analogicznie, tylko odejmowania i nierówności w drugą stronę
    elif(trend<0):                
        for i in range (len(H)-1):
            if(L[i]>H[i+1]):
                gaps.append( (i,L[i+1]+(H[i]-L[i+1])/2.) )            
    else: 
        return None                        