# coding: utf-8
"""Dane wejściowe do każdej funkcji to 4 tablice jednakowej długości przechowujące
kursy open, low, high, close. Parament trend oznacza to, w jakim trendzie się znajdujemy,
(rosnący lub malejący). Roboczo przekazuję jako string, ale to kwestia ustalenia.
"""

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
    if trend=='rising':
        result.append(findBull3(O,H,L,C))        
        result.append(findEveningStar(O,H,L,C))                
        result.append(findDarkCloud(O,H,L,C))
    else:
        result.append(findBear3(O,H,L,C))        
        result.append(findMorningStar(O,H,L,C))                 
        result.append(findPiercing(O,H,L,C))
    return [value for value in result if value != None]

"""Algorytm szukania każdej formacji jest identyczny: lecimy od końca i sprawdzamy po kolei
świeczki czy są takie jak formacja nakazuje. Jeśli znajdziemy coś dobrego to kończymy 
(nie interesuje nas co było wcześniej), jeśli nie to zwracamy None"""    

def findDarkCloud(O,H,L,C):
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

def findPiercing(O,H,L,C):
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

def findEveningStar(O,H,L,C):
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

def findMorningStar(O,H,L,C):
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

"""luki i wyspy traktuję jako osobną rzecz od formacji świecowych 
(podobnie zresztą jak literatura)
po pierwsze nie wymagają świec (wystarczy zwykły wykres słupkowy), 
po drugie kształtują się przez dłuższy czas, więc są IMO ważniejsze"""

def findIsland(O,H,L,C,trend):
    """Znajduje formację wyspy. Jest to formacja odwrócenia trendu"""
    pass

def findGaps(O,H,L,C,trend):
    """Znajduje na danej tablicy lukę startową, ucieczki i wyczerpania. 
    Używać najlepiej po wybiciu z formacji."""
    pass

#(breakaway gaps)  (continuation gaps)  (exhaustion gaps)