# -*- coding: utf-8 -*-
__author__ = "Xai"
__date__ = "$2012-03-02 19:32:01$"

import numpy as np
import re
import csv
import datetime
import urllib2
import cStringIO

#ZMIENNE GLOBALNE
DATABASE_LAST_UPDATE = datetime.date(2012,1,1)
INDEX_LIST = []
STOCK_LIST = []
FOREX_LIST = []


class FinancialObject(object):
	"""Klasa definiująca obiekt finansowy (index,spółkę,surowiec,obligację, etc.), w której przechowywane będą archiwalne notowania i 		   być może obliczone wskaźniki. """
	
	def __init__ (self, name, abbreviation, financialType, dataSource, detail = None,lastUpdate = datetime.date(1971,1,1)):
		self.name = name
		self.abbreviation = abbreviation 
		self.financialType = financialType
		self.dataSource = dataSource
		self.detail = detail #Informacja szczegółowa -> Index - kraj / Społka - index
		self.lastUpdate = lastUpdate
		self.currentValue = [] #para wartość i data pobrania
		self.previousValues = []  #lista w wartości z tego samego dnia ale pobranych wcześniej postaci: [datetime, value]
		self.valuesDaily = [] #lista list w przypadku yahoo postaci [[date,open,high,low,close,volume,adj close], [date, ...], ...] 
					# w przypadku Stooq bez adj close.
		self.valuesWeekly = [] # jak wyżej tylko dla danych tygodniowych
		self.valuesMonthly = [] # jak wyżej tylko dla danych miesięcznych

	def getCurrentValue(self):
		"""Metoda aktualizująca dane dotyczące aktualnej wartości obiektu oraz przenosząca poprzednią wartość do listy poprzednich wartości"""
		day = datetime.timedelta(days=1)
		lastUpdate = self.lastUpdate + day
		if self.dataSource == "Yahoo":
			tmpObj = createWithCurrentValueFromYahoo(self.name, self.abbreviation, self.financialType, self.detail)
		elif self.dataSource == "Stooq":
			tmpObj = createWithCurrentValueFromStooq(self.name, self.abbreviation, self.financialType,self.detail)
		self.previousValues = self.previousValues + self.currentValue
		self.currentValue = tmpObj.currentValue

	def updateArchive(self):
		"""Metoda aktualizująca dane istniejącego obiektu. Tworzy nowy tymczasowy obiekt i kopiuje jego zawartość do obiektu 'self'. """
		day = datetime.timedelta(days=1)
		lastUpdate = self.lastUpdate + day
		if self.dataSource == "Yahoo":
			tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, lastUpdate)
		elif self.dataSource == "Stooq":
			tmpObj = createWithArchivesFromStooq(self.name, self.abbreviation, self.financialType, lastUpdate)
		self.valuesDaily = self.valuesDaily + tmpObj.valuesDaily
		self.valuesWeekly = self.valuesWeekly + tmpObj.valuesWeekly
		self.valuesMonthly = self.valuesMonthly + tmpObj.valuesMonthly

	def getArray(self, time):

		"""Funkcja zwracająca rekordowaną tablicę (numpy.recarray) dla informacji w odstępie czasu przekazanym jako parametr funkcji. Pozwala to dostać się do poszczególnych tablic używając odpowiednich rekordów: 'date' 'open' etc."""

		if self.financialType == 'forex':
			tmplist = []
			if time == 'daily':
				for x in self.valuesDaily:
					tmplist = tmplist + [(str(x[0]),x[1],x[2],x[3],x[4])]
			if time == 'weekly':
				for x in self.valuesWeekly:
					tmplist = tmplist + [(str(x[0]),x[1],x[2],x[3],x[4])]
			if time == 'monthly':
				for x in self.valuesMonthly:
					tmplist = tmplist + [(str(x[0]),x[1],x[2],x[3],x[4])]
			return np.array(tmplist,dtype = [('date','S10'),('open',float),('high',float),('low',float),('close',float)])
		else:
			tmplist = []
			if time == 'daily':
				for x in self.valuesDaily:
					tmplist = tmplist + [(str(x[0]),x[1],x[2],x[3],x[4],x[5])]
			if time == 'weekly':
				for x in self.valuesWeekly:
					tmplist = tmplist + [(str(x[0]),x[1],x[2],x[3],x[4],x[5])]
			if time == 'monthly':
				for x in self.valuesMonthly:
					tmplist = tmplist + [(str(x[0]),x[1],x[2],x[3],x[4],x[5])]
			return np.array(tmplist,dtype = [('date','S10'),('open',float),('high',float),('low',float),('close',float),('volume',int)])
			
	def getIndex(self, begin, end, time = 'daily'):
		"""Funkcja zwracająca indeksy tablicy dla danego przedziału czasu"""
		if time == 'daily':
			finish = 0
			while (end < self.valuesDaily[finish][0]):
				finish += 1
			start = finish
			while (begin < self.valuesDaily[start][0]):
				start += 1
			return [finish,start]
		if time == 'weekly':
			finish = 0
			while (end < self.valuesWeekly[finish][0]):
				finish += 1
			start = finish
			while (begin < self.valuesWeekly[start][0]):
				start += 1
			return [finish,start]
		if time == 'monthly':
			finish = 0
			while (end < self.valuesMonthly[finish][0]):
				finish += 1
			start = finish
			while (begin < self.valuesMonthly[start][0]):
				start += 1
			return [finish,start]
#koniec definicji klasy

def createWithCurrentValueFromYahoo(name, abbreviation, financialType, detail):
	"""Funkcja tworząca obiekt zawierający aktualną na daną chwilę wartość ze strony finance.yahoo"""

	finObj = FinancialObject(name,abbreviation, financialType, "Yahoo", detail)

	url = "http://finance.yahoo.com/q?s="+abbreviation
	try:
		site = urllib2.urlopen(url)
	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return
	pageSource = site.read()
	if abbreviation[0] == '^':
		pattern = '\\'+abbreviation.lower()+'">([0-9]*,*[0-9]+\.*[0-9]+)<'
	else:	
		pattern = abbreviation.lower()+'">([0-9]*,*[0-9]+\.*[0-9]+)<'
	pattern = re.compile(pattern)
	m = re.search(pattern,pageSource)
	
	timeNow = datetime.datetime.now()
	finObj.currentValue = [float(m.group(1).replace(',','')),timeNow]
	return finObj

def createWithCurrentValueFromStooq(name, abbreviation, financialType, detail):
	"""Funkcja tworząca obiekt zawierający aktualną na daną chwilę wartość ze strony Stooq.pl"""

	finObj = FinancialObject(name,abbreviation, financialType, "Stooq", detail)

	url = "http://stooq.pl/q/g/?s="+abbreviation.lower()
	try:
		site = urllib2.urlopen(url)
	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return
	pageSource = site.read()
	pattern = '_c[0-9]>([0-9]*,*[0-9]+\.*[0-9]+)<'
	pattern = re.compile(pattern)
	m = re.search(pattern,pageSource)
	timeNow = datetime.datetime.now()
	finObj.currentValue = [float(m.group(1).replace(',','')),timeNow]
	return finObj

def createWithArchivesFromYahoo(name, abbreviation, financialType, detail, sinceDate = datetime.date(1971,1,1)):
	"""Funkcja tworząca obiekt zawierający archiwalne dane pobrane ze strony finance.yahoo dotyczące obiektu zdefiniowanego w parametrach funkcji"""
	currentDate = datetime.date.today()
	finObj = FinancialObject(name,abbreviation, financialType, "Yahoo", detail, currentDate)

	# DAILY
	url = 'http://ichart.finance.yahoo.com/table.csv?s='+abbreviation+'&a='+str(sinceDate.day)+'&b='+str(sinceDate.month-1)	 
        url = url+'&c='+str(sinceDate.year)+'&d='+str(currentDate.month-1)+'&e='
	url = url+str(currentDate.day)+'&f='+str(currentDate.year)+'&g=d&ignore=.csv'
	try:
		site = urllib2.urlopen(url)
	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return

	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])]]
		finObj.valuesDaily = finObj.valuesDaily + dataRow

	#WEEKLY
	url = url.replace('&g=d', '&g=w')
	site = urllib2.urlopen(url)
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])]]
		finObj.valuesWeekly = finObj.valuesWeekly + dataRow

	#MONTHLY
	url = url.replace('&g=w', '&g=m')
	site = urllib2.urlopen(url)
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])]]
		finObj.valuesMonthly = finObj.valuesMonthly + dataRow

	return finObj

def createWithArchivesFromStooq(name, abbreviation, financialType, detail, sinceDate = datetime.date(1971,1,1)):
	"""Funkcja tworząca obiekt zawierający aktualną na daną chwilę wartość ze strony stooq.pl"""

	finObj = FinancialObject(name,abbreviation, financialType, detail, "Stooq")
	currentDate = datetime.date.today()

	try:
		url= 'http://stooq.pl/q/d/?s='+abbreviation.lower()
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		site = opener.open(url)
		x = site.info()['Set-Cookie']
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Referer','http://stooq.pl/q/d/?s=08n'),('Host','stooq.p')]
		opener.addheaders = [('Cookie', x)]
		url2 = 'http://stooq.pl/q/d/l/?s='+abbreviation.lower()+'&d1='+parserDateToString(sinceDate)+'&d2='
		url2 = url2 + parserDateToString(currentDate)+'&i=d'
		site = opener.open(url2)

	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		if financialType == 'forex':
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4])]]
		else:
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]]	
		finObj.valuesDaily = finObj.valuesDaily + dataRow

	#WEEKLY
	url2 = url2.replace('&i=d', '&i=w')
	site = opener.open(url2)
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		if financialType == 'forex':
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4])]]
		else:
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]]	
		finObj.valuesWeekly = finObj.valuesWeekly + dataRow

	#MONTHLY
	url2 = url2.replace('&i=w', '&i=m')
	site = opener.open(url2)
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		if financialType == 'forex':
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4])]]
		else:
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]]	
		finObj.valuesMonthly = finObj.valuesMonthly + dataRow
	return finObj
	
	 
def parserStringToDate(string):
	"""Funkcja zmieniająca ciąg znaków postaci "YYYY-MM-DD" na obiekt klasy datatime.date"""
	string = string.split('-')
	x = datetime.date(int(string[0]),int(string[1]),int(string[2]))
	return x

def parserDateToString(date):
	"""Funkcja zmieniająca obiekt datetime.date na string postaci YYYYMMDD"""
	date = str(date)
	date = date.replace('-','')
	return date

def updateDatabase():
	"""Funkcja sprawdzająca czy na rynkach pojawiły się nowe spółki, jeśli tak to dodaje spółki do bazy danych. """
	month = DATABASE_LAST_UPDATE.ctime()[4:7:1]
	year = DATABASE_LAST_UPDATE.year%100

	url = "http://biz.yahoo.com/ipo/prc_"+month.lower()+str(year)+".html"
	try:
		site = urllib2.urlopen(url)
	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return
	pageSource = site.read()
	pattern = '(?s)Prev(.*)Prev'
	pattern = re.compile(pattern)
	m = re.search(pattern,pageSource)
	pageSource = m.group(0)

	pattern = '>([0-9][0-9]*-[A-Z][a-z][a-z]-[0-9][0-9])</td><td>(.*)</td><td.*>([A-Z][A-Z][A-Z]*)<.*>M<'
	for m in re.finditer(pattern,pageSource):
		print m.group(1) + m.group(2) + m.group(3)

def loadData():
	"""Funkcja wczytująca dane z 'bazy danych' na temat dostępnych do wyszukania obiektów finansowych i zapisuje je do zmiennych globalnych""" 
	global INDEX_LIST
	global STOCK_LIST
	global FOREX_LIST
	global DATABASE_LAST_UPDATE
	csvFile  = open('data1.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		INDEX_LIST = INDEX_LIST + [[row[0],row[1],row[2],'America']]
	
	csvFile  = open('data2.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	flag = True
	for row in dataCsv:
		if flag == True:
			DATABASE_LAST_UPDATE = parserStringToDate(row[1])
			flag = False
		else:	
			STOCK_LIST = STOCK_LIST + [[row[0],row[1],row[2],row[3]]]
	
	csvFile  = open('data3.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		FOREX_LIST = FOREX_LIST + [[row[0],row[1],row[2],row[3]]]


def getAdvDec(date):
	"""Funkcja zwracająca listę krotek postaci(LICZBA_WZROSTÓW,LICZBA_SPADKÓW,LICZBA_BEZZMIAN) dla indeksów NYSE, AMEX, NASDAQ"""
	list = []
	url = 'http://unicorn.us.com/advdec/'+ str(date.year)+'/adu'+ parserDateToString(date) +'.txt'
	try:
		site = urllib2.urlopen(url)
	except urllib2.HTTPError, ex:
		if ex.code == 404:
			print "Nie można pobrać danych. Rynki mogłybyć nie czynne w tym dniu."
			return [[0,0,0],[0,0,0],[0,0,0]]
		return
	pageSource = site.read()
	pageSource = pageSource.replace(' ','')
	csvString = cStringIO.StringIO(pageSource)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	dataCsv.next()
	for row in dataCsv:
		list += [[row[1],row[2],row[3]]]
	return list
	
def getAdvDecInPeriodOfTime(begin,end,index):
	tmplist = []
	day = datetime.timedelta(days=1)
	if index == 'NYSE':
		while(begin != end):
			x = getAdvDec(begin)
			tmplist += [tuple([str(begin)]+x[0])]
			begin += day
		return np.array(tmplist,dtype = [('date','S10'),('adv',int),('dec',int),('unc',int)])
	if index == 'AMEX':
		while(begin != end):
			x = getAdvDec(begin)
			tmplist += [tuple([str(begin)]+x[1])]
			begin += day
		return np.array(tmplist,dtype = [('date','S10'),('adv',int),('dec',int),('unc',int)])
	if index == 'NASDAQ':
		while(begin != end):
			x = getAdvDec(begin)
			tmplist += [tuple([str(begin)]+x[2])]
			begin += day
		return np.array(tmplist,dtype = [('date','S10'),('adv',int),('dec',int),('unc',int)])


"""for x in US_INDICES:
	print x[1]+','+x[0]+',Yahoo'""" """
x = createWithCurrentValueFromStooq('USD/GPB', 'plngbp', 'forex', 'gbp')
x.getCurrentValue()
print x.currentValue
print x.previousValues
for k in x.valuesMonthly:
	print k 
updateDatabase()
"""
"""
loadData()
i = 1
for x in FOREX_LIST:
	i = i+1
	x = createWithArchivesFromStooq(x[1],x[0],'forex',x[3])
	print DATABASE_LAST_UPDATE
"""
"""
csvFile  = open('companylist(1).csv', "rb")
dataCsv = csv.reader(csvFile)
dataCsv.next()
i = 0
for row in dataCsv:
	print row[0]+','+row[1]+',Yahoo,AMEX'
"""
"""
### PRZYKŁADOWE UŻYCIE ###
loadData() #Wczytuje dane do zmiennych globalnych

#załóżmy, że użytkownik chce informacje dotyczące "21Vianet Group Inc."

finObj = createWithCurrentValueFromYahoo(STOCK_LIST[6][1],STOCK_LIST[6][0],'stock',STOCK_LIST[6][3]) #tworzymy obiekt z aktualną wartością akcji

finObj.updateArchive() #pobieramy wartości archiwalne do obiektu
print "Aktualna wartość: " + str(finObj.currentValue[0])

a = finObj.getArray('daily')
print a['date']

x = finObj.getIndex(datetime.date(2011,8,8),datetime.date(2012,2,17),'daily')
print x
print finObj.valuesDaily[x[0]][0]
print finObj.valuesDaily[x[1]][0]
<<<<<<< HEAD
=======


#x = getAdvDecInPeriodOfTime(datetime.date(2003,7,10),datetime.date(2004,2,2),'NYSE')

#print x['adv']
<<<<<<< HEAD
>>>>>>> chart
"""
=======
"""
>>>>>>> 7e45d72b6b6818199f385fa69d03d21f28bcd265
