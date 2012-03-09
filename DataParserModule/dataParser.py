# -*- coding: utf-8 -*-
__author__ = "Xai"
__date__ = "$2012-03-02 19:32:01$"

import numpy as np
import re
import csv
import datetime
import urllib2
import cStringIO

#Lista indeksów US
US_INDICES = [["Dow Jones Composite Average", "^DJA"], ["Dow Jones Industrial Average", "^DJI"], ["Dow Jones Transportation Average", "^DJT"], ["Dow Jones Utility Average", "^DJU"],["NYSE COMPOSITE INDEX","^NYA"],["NYSE International 100","^NYI"], ["NYSE TMT","^NYY"], ["NYSE US 100","^NY"], ["NYSE World Leaders","^NYL"], ["NASDAQ Bank","^IXBK"], ["NASDAQ Biotechnology","^NBI"], ["NASDAQ Composite","^IXIC"], ["NASDAQ Computer","^IXK"], ["NASDAQ Financial 100","^IXF"], ["NASDAQ Industrial","^IXID"], ["NASDAQ Insurance","^IXIS"], ["NASDAQ Other Finance","^IXFN"], ["NASDAQ Telecommunications","^IXUT"], ["NASDAQ Transportation","^IXTR"], ["NASDAQ-100","^NDX"], ["S&P 100 INDEX","^OEX"],  ["S&P 400 MIDCAP INDEX","^MID"],  ["S&P 500","^GSPC"],  ["S&P COMPOSITE 1500 INDEX","^SPSUPX"],  ["S&P SMALLCAP 600 INDEX","^SML"], ["AMEX COMPOSITE INDEX","^XAX"], ["AMEX INTERACTIVE WEEK INTERNET","^IIX"], ["AMEX NETWORKING INDEX","^NWX"], ["DJUS Market Index (full-cap)","^DWC"], ["MAJOR MARKET INDEX","^XMI"], ["NYSE Arca Tech 100 Index","^PSE"], ["PHLX Semiconductor","^SOX"], ["Russell 1000","^RUI"], ["Russell 2000","^RUT"], ["Russell 3000","^RUA"], ["13-WEEK TREASURY BILL","^IRX"], ["CBOE Interest Rate 10-Year T-No","^TNX"], ["Treasury Yield 30 Years","^TYX"], ["Treasury Yield 5 Years","^FVX"], ["PHLX Gold/Silver Sector", "^XAU"]]

#Brak danych: ["BATS 1000 Index","^BATSK"]


class FinancialObject:
	"""Klasa definiująca obiekt finansowy (index,spółkę,surowiec,obligację, etc.), w której przechowywane będą archiwalne notowania i 		   być może obliczone wskaźniki. """
	
	def __init__ (self, name, abbreviation, financialType, dataSource, lastUpdate = datetime.date(1971,1,1)):
		self.name = name
		self.abbreviation = abbreviation 
		self.financialType = financialType
		self.dataSource = dataSource
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
			tmpObj = createWithCurrentValueFromYahoo(self.name, self.abbreviation, self.financialType)
		elif self.dataSource == "Stooq":
			tmpObj = createWithCurrentValueFromStooq(self.name, self.abbreviation, self.financialType)
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
#koniec definicji klasy

def createWithCurrentValueFromYahoo(name, abbreviation, financialType):
	"""Funkcja tworząca obiekt zawierający aktualną na daną chwilę wartość ze strony finance.yahoo"""

	finObj = FinancialObject(name,abbreviation, financialType, "Yahoo")

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

def createWithCurrentValueFromStooq(name, abbreviation, financialType):
	"""Funkcja tworząca obiekt zawierający aktualną na daną chwilę wartość ze strony Stooq.pl"""

	finObj = FinancialObject(name,abbreviation, financialType, "Stooq")

	url = "http://stooq.pl/q/g/?s="+abbreviation.lower()
	try:
		site = urllib2.urlopen(url)
	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return
	pageSource = site.read()
	pattern = '_c2>([0-9]*,*[0-9]+\.*[0-9]+)<'
	pattern = re.compile(pattern)
	m = re.search(pattern,pageSource)
	timeNow = datetime.datetime.now()
	finObj.currentValue = [float(m.group(1).replace(',','')),timeNow]
	return finObj

def createWithArchivesFromYahoo(name, abbreviation, financialType, sinceDate = datetime.date(1971,1,1)):
	"""Funkcja tworząca obiekt zawierający archiwalne dane pobrane ze strony finance.yahoo dotyczące obiektu zdefiniowanego w parametrach funkcji"""
	currentDate = datetime.date.today()
	finObj = FinancialObject(name,abbreviation, financialType, "Yahoo", currentDate)

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

def createWithArchivesFromStooq(name, abbreviation, financialType, sinceDate = datetime.date(1971,1,1)):
	"""Funkcja tworząca obiekt zawierający aktualną na daną chwilę wartość ze strony stooq.pl"""

	finObj = FinancialObject(name,abbreviation, financialType, "Stooq")
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
		print url2
		site = opener.open(url2)

	except urllib2.URLError, ex:
		print "Something wrong happend! Check your internet connection!"
		return
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]]
		finObj.valuesDaily = finObj.valuesDaily + dataRow

	#WEEKLY
	url2 = url2.replace('&i=d', '&i=w')
	site = opener.open(url2)
	csvString = site.read()
	print csvString
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
		dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]]
		finObj.valuesWeekly = finObj.valuesWeekly + dataRow

	#MONTHLY
	url2 = url2.replace('&i=w', '&i=m')
	print url2
	site = opener.open(url2)
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	for row in dataCsv:
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
	pass


#for x in US_INDICES:
	#print x[1]
x = createWithCurrentValueFromStooq('Octava', 'BPH', 'stock')
x.getCurrentValue()
print x.currentValue
print x.previousValues
for k in x.valuesMonthly:
	print k 







