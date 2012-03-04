# -*- coding: utf-8 -*-
__author__ = "Xai"
__date__ = "$2012-03-02 19:32:01$"

import numpy as np
import csv
import datetime
import urllib2
import cStringIO

#Lista indeksów US
US_INDICES = [["Dow Jones Composite Average", "^DJA"], ["Dow Jones Industrial Average", "^DJI"], ["Dow Jones Transportation Average", "^DJT"], ["Dow Jones Utility Average", "^DJU"],["NYSE COMPOSITE INDEX","^NYA"],["NYSE International 100","^NIN"], ["NYSE TMT","^NTM"], ["NYSE US 100","^NUS"], ["NYSE World Leaders","^NWL"], ["NASDAQ Bank","^IXBK"], ["NASDAQ Biotechnology","^NBI"], ["NASDAQ Composite","^IXIC"], ["NASDAQ Computer","^IXK"], ["NASDAQ Financial 100","^IXF"], ["NASDAQ Industrial","^IXID"], ["NASDAQ Insurance","^IXIS"], ["NASDAQ Other Finance","^IXFN"], ["NASDAQ Telecommunications","^IXUT"], ["NASDAQ Transportation","^IXTR"], ["NASDAQ-100","^NDX"], ["S&P 100 INDEX","^OEX"],  ["S&P 400 MIDCAP INDEX","^MID"],  ["S&P 500","^GSPC"],  ["S&P COMPOSITE 1500 INDEX","^SPSUPX"],  ["S&P SMALLCAP 600 INDEX","^SML"], ["AMEX COMPOSITE INDEX","^XAX"], ["AMEX INTERACTIVE WEEK INTERNET","^IIX"], ["AMEX NETWORKING INDEX","^NWX"], ["DJUS Market Index (full-cap)","^DWC"], ["MAJOR MARKET INDEX","^XMI"], ["NYSE Arca Tech 100 Index","^PSE"], ["PHLX Semiconductor","^SOX"], ["Russell 1000","^RUI"], ["Russell 2000","^RUT"], ["Russell 3000","^RUA"], ["13-WEEK TREASURY BILL","^IRX"], ["CBOE Interest Rate 10-Year T-No","^TNX"], ["Treasury Yield 30 Years","^TYX"], ["Treasury Yield 5 Years","^FVX"], ["PHLX Gold/Silver Sector", "^XAU"]]

#Brak danych: ["BATS 1000 Index","^BATSK"]


class FinancialObject:
	"""Klasa definiująca obiekt finansowy (index,spółkę,surowiec,obligację, etc.), w której przechowywane będą archiwalne notowania i 		   być może obliczone wskaźniki. """
	
	def __init__ (self, name, abbreviation, financialType, dataSource, lastUpdate):
		self.name = name
		self.abbreviation = abbreviation 
		self.financialType = financialType
		self.dataSource = dataSource
		self.lastUpdate = lastUpdate
		self.valuesDaily = [] #lista list w przypadku yahoo postaci [[date,open,high,low,close,volume,adj close], [date, ...], ...] 
		self.valuesWeekly = [] # jak wyżej tylko dla danych tygodniowych
		self.valuesMonthly = [] # jak wyżej tylko dla danych miesięcznych

	def update(self):
		"""Metoda aktualizująca dane istniejącego obiektu. Tworzy nowy tymczasowy obiekt i kopiuje jego zawartość do obiektu 'self'. """
		day = datetime.timedelta(days=1)
		lastUpdate = self.lastUpdate + day
		if self.dataSource == "Yahoo":
			tmpObj = getFromYahoo(self.name, self.abbreviation, self.financialType, lastUpdate)
			self.valuesDaily = self.valuesDaily + tmpObj.valuesDaily
			self.valuesWeekly = self.valuesWeekly + tmpObj.valuesWeekly
			self.valuesMonthly = self.valuesMonthly + tmpObj.valuesMonthly
			
			


#koniec definicji klasy


def getFromYahoo(name, abbreviation, financialType, sinceDate = datetime.date(1971,1,1)):
	"""Funkcja pobierająca dane ze strony finance.yahoo dotyczące obiektu zdefiniowanego w parametrach funkcji"""
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
		dataRow = [[parserDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])]]
		finObj.valuesDaily = finObj.valuesDaily + dataRow

	#WEEKLY
	url = url.replace('&g=d', '&g=w')
	site = urllib2.urlopen(url)
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	#i = 0
	for row in dataCsv:
		dataRow = [[parserDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])]]
		finObj.valuesWeekly = finObj.valuesDaily + dataRow

	#MONTHLY
	url = url.replace('&g=d', '&g=w')
	site = urllib2.urlopen(url)
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	
	dataCsv = csv.reader(csvString)
	dataCsv.next()
	#i = 0
	for row in dataCsv:
		dataRow = [[parserDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6])]]
		finObj.valuesMonthly = finObj.valuesDaily + dataRow

	return finObj

	
 


def parserDate(string):
	"""Funkcja zmieniająca ciąg znaków postaci "YYYY-MM-DD" na obiekt klasy datatime.date"""
	string = string.split('-')
	x = datetime.date(int(string[0]),int(string[1]),int(string[2]))
	return x


for x in US_INDICES:
	print x[1]
	getFromYahoo(x[0],x[1],'index')
	




