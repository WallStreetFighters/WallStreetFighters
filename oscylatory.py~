from numpy import *

# funkcja liczy zwyczajna srednia artmetyczna z podanej jej tablicy, przekazywac tablice jednowymiarowa!
def simpleArthmeticAverage(array):
	result = 0
	for i in range(array.size):
		result += array[i]
	result /= array.size
	return result

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

# Srednie odchylenie tablicy
def meanDeviation(array):
	result = 0
	average = simpleArthmeticAverage(array)
	for i in range(0,array.size):
		temp = array[i] - average
		if temp<0:
			temp = -1*temp
		result += temp
	result /= array.size
	return result

# Funkcja zwraca tablice z wartosciami wskaznika Comodity Index Channel, dlugosc tablicy jest rowna
# closeTable.size-duration
def CCI(closeTable,lowTable,highTable,duration):
	size = closeTable.size
	typicalPricesTable = zeros(size)
	for i in range(0,size):
		typicalPricesTable[i] = (closeTable[i]+lowTable[i]+highTable[i])/3
	values = zeros(size-duration)
	j = 0
	for i in range(duration,size):
		tempTypical = typicalPricesTable[i-duration:i+1]
		average = simpleArthmeticAverage(tempTypical)
		deviation = meanDeviation(tempTypical)
		print deviation
		values[j] = (typicalPricesTable[i] - average)/(0.015*deviation)
		j += 1
	return typicalPricesTable

# funkcja testujaca CCI, wartosci wziete stad http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci		
def test():
	high = array([24.2,24.07,24.04,23.87,23.67,23.59,23.8,23.8,24.3,24.15,24.05,24.06,23.88,25.14,25.2,25.07,25.22,25.37,25.36,25.26,24.82,24.44,24.65,24.84,24.75,24.51,24.68,24.67,23.84,24.3])
	low = array([23.85,23.72,23.64,23.37,23.46,23.18,23.4,23.57,24.05,23.77,23.6,23.84,23.64,23.94,24.74,24.77,24.9,24.93,24.96,24.93,24.21,24.21,24.43,24.44,24.2,24.25,24.21,24.15,23.63,23.76])
	close = array([23.89,23.95,23.67,23.78,23.5,23.32,23.75,23.79,24.14,23.81,23.78,23.86,23.7,24.96,24.88,24.96,25.18,25.07,25.27,25.0,24.46,24.28,24.62,24.58,24.53,24.35,24.34,24.23,23.76,24.2])
	result = CCI(close,low,high,20)
	return result
