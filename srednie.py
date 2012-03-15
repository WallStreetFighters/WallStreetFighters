from numpy import *
import math

# funkcja liczy zwyczajna srednia artmetyczna z podanej jej tablicy, przekazywac tablice jednowymiarowa!
def simpleArthmeticAverage(array):
	result = 0
	for i in range(array.size):
		result += array[i]
	result /= array.size
	return result

# liczy srednia wazona gdzie najmniejsza wage = 1 ma pierwszy element, najwieksza wage element ostatni z waga rowna dlugosci tablicy
def weightedAverage(array):
	result = 0
	tableSum = arange(1,array.size+1,1)
	divisor = tableSum.sum()
	for i in range(array.size):
		result += array[i]*(i+1)
	result /= divisor
	return result

# liczy srednia expotencjalna gdzie alfa = 2/(1+N)
# Najwiekszy 'potencjal' ma wartosc ostatnia, pierwsza wartosc ma potencjal (1-alfa)^N
def expotentialAverage(array):
	result = 0
	divisor = 0
	factor = 2.0/(array.size+1)
	for i in range(array.size):
		result += array[i]*((1-factor)**(array.size-i-1))
		divisor += (1-factor)**(array.size-i-1)
	result /= divisor
	return result

# array - tablica z wartosciami cen zamkniec itp, duration - czas trwania liczonej sredniej krokowej
# Zwraca tablice jednowymiarowa z wartosciami sredniej krokowej dla przedzialu [size/2,size-1], aby obliczyc wartosci tablica wejsciowa musi byc 2x wieksza od zakresu(duration)
# modes : 1-SMA(simple moving average), 2-WMA(weighted moving average), 3-EMA(expotential moving average) 
def movingAverage(array,duration,mode):
	values = zeros(duration)
	size = array.size
	j = 0
	for i in range(size/2,size):
		tempTable = array[i-duration+1:i+1]
		if mode == 1:
			values[j] = simpleArthmeticAverage(tempTable)
		if mode == 2:
			values[j] = weightedAverage(tempTable)
		if mode == 3:
			values[j] = expotentialAverage(tempTable)
		j += 1
		if j == values.size:
			break
	return values

# Indeks new High/new Low. Zwraca pojedyncza wartosc, przekazujemy zazwyczaj tablice zamkniec gieldy.
def highLowIndex(array):
	size = array.size
	highest = array[0]
	lowest = array[0]
	numberOfHighest = 1.0
	numberOfLowest = 1.0
	for i in range(1,size):
		if array[i] > highest:
			highest = array[i]
			numberOfHighest += 1.0
		if array[i] < lowest:
			lowest = array[i]
			numberOfLowest += 1.0
	return (numberOfHighest/(numberOfHighest+numberOfLowest))*100

# Standardowe odchylenie dla tablicy array, koniecznie jednowymiarowa
def standardDeviation(array):
	size = array.size
	average = simpleArthmeticAverage(array)
	total = 0
	for i in range(0,size):
		total += (array[i] - average)**2
	total /= size
	total = math.sqrt(total)
	return total

# Oblicza tablice wartosci Wsteg Bollingera :
# array - wartosci gieldowe(najlepiej kolejne zamkniecia gield)
# duration - okres obliczanego wskaznika, WAZNE ABY array BYLA 2x WIEKSZA NIZ duration (patrz movingAverage)
# mode - 1: Gorna wstega Bollingera, 2: Dolna wstega Bollingera
# D - stala uzywana do odchylania wsteg, domyslnie 2
def bollingerBands(array,duration,mode,D):
	values = zeros(duration)
	size = array.size
	j = 0
	for i in range(size/2,size):
		tempTable = array[i-duration+1:i+1]
		if mode == 1:
			values[j] = simpleArthmeticAverage(tempTable)+(D*standardDeviation(tempTable))
		if mode == 2:
			values[j] = simpleArthmeticAverage(tempTable)-(D*standardDeviation(tempTable))
		j += 1
		if j == values.size:
			break
	return values
			





	
	
