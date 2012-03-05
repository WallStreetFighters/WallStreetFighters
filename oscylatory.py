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
	values = zeros(size-duration+1)
	j = 0
	for i in range(duration-1,size):
		tempTypical = typicalPricesTable[i-duration+1:i+1]
		average = simpleArthmeticAverage(tempTypical)
		deviation = meanDeviation(tempTypical)
		values[j] = (typicalPricesTable[i] - average)/(0.015*deviation)
		j += 1
	return values

# funkcja testujaca CCI, wartosci wziete stad http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci		
def test():
	high = array([24.2,24.07,24.04,23.87,23.67,23.59,23.8,23.8,24.3,24.15,24.05,24.06,23.88,25.14,25.2,25.07,25.22,25.37,25.36,25.26,24.82,24.44,24.65,24.84,24.75,24.51,24.68,24.67,23.84,24.3])
	low = array([23.85,23.72,23.64,23.37,23.46,23.18,23.4,23.57,24.05,23.77,23.6,23.84,23.64,23.94,24.74,24.77,24.9,24.93,24.96,24.93,24.21,24.21,24.43,24.44,24.2,24.25,24.21,24.15,23.63,23.76])
	close = array([23.89,23.95,23.67,23.78,23.5,23.32,23.75,23.79,24.14,23.81,23.78,23.86,23.7,24.96,24.88,24.96,25.18,25.07,25.27,25.0,24.46,24.28,24.62,24.58,24.53,24.35,24.34,24.23,23.76,24.2])
	result = CCI(close,low,high,20)
	return result

# Korzysta z niej RSI, sumuje elementy tablicy i w zaleznosci od mode, zmienia znak lub nie :)
def sumUnderCondition(array,mode):
        result = 0
        size = array.size
        if mode == 1:
                for i in range(0,size):
                        if array[i] >= 0:
                                result += array[i]
        if mode == 2:
                for i in range(0,size):
                        if array[i] <= 0:
                                result += array[i]
                result *= -1
        return result

# Liczy wskaznik RSI, przekazujemy wartosci najlepiej zamkniec sesji, otrzymujemy tablice
# wielkosci array-duration ze wartosciami RSI dla indeksow tablicy [duration,size]
def RSI(array, duration):
        size = array.size
        values = zeros(size-duration)
        gainLossTable = zeros(size)
        for i in range(1,size):
                gainLossTable[i-1] = array[i]-array[i-1]
        k = 0
        averageGain = (sumUnderCondition(gainLossTable[0:duration-1],1))/duration
        averageLoss = (sumUnderCondition(gainLossTable[0:duration-1],2))/duration
        for j in range(duration,size):    
                RS = averageGain/averageLoss
                RSI = 100.0 - (100.0/(1+RS))
                values[k] = RSI
                k += 1
                if j < size:
                        if gainLossTable[j] > 0:
                                averageGain = (averageGain*13 + gainLossTable[j])/14.0
                                averageLoss = (averageLoss*13 + 0)/14.0
                        if gainLossTable[j] <= 0:
                                averageGain = (averageGain*13 + 0)/14.0
                                averageLoss = (averageLoss*13 + (-1)*gainLossTable[j])/14.0
        return values
# Funkcja do testowania poprawnych wynikow wskaznika RSI, wartosci pobrane z http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
def testRSI():
        a = array([44.34,44.09,44.15,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.0,46.03,46.41,46.22,45.64,46.21,46.25,45.71,46.45,45.78,45.35,44.03,44.18,44.22,44.57,43.42,42.66,43.13])
        result = RSI(a,14)
        return result


