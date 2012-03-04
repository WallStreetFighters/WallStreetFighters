from numpy import *

# Zwraca tablice wartosci wskaznika Impetu(Momentum) dla danej tablicy. Co wazne, ilosc obliczonych wartosci to rozmiar tablicy - duration
def momentum(array,duration):
	values = zeros(array.size-duration)
	size = array.size
	j = 0
	for i in range(duration,size):
		values[j] = array[i] - array[i-duration]
		j += 1
	return values

# Jak wyzej
def ROC(array, duration):
	values = zeros(array.size-duration)
	size = array.size
	j = 0
	for i in range(duration,size):
		values[j] = ((array[i] - array[i-duration])/(array[i-duration]))*100
		j += 1
	return values
