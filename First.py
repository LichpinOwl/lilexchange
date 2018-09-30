# -*- coding: utf-8 -*-
from lxml import html
import requests
import os
import time
import sqlite3
from datetime import datetime

cwd = os.path.dirname(os.path.abspath(__file__)) + "\\"

AllPriceList = []

ClosePriceList = [] 

PairsList = ['USD_NAGHDI', 'USD_SARRAFI', 'EUR', 'USD_STANBUL', 'USD_SOLEIMANIEH', 'USD_HARAT', 'USD_BUSHEHR' , 
			 'USD_SHIRAZ', 'USD_MASHHAD', 'USD_PIRANSHAHR', 'USD_BANEH', 'USD_MARIWAN', 'USD_TBILISI', 
			 'USD_GEORGIA_HAVALEH', 'USD_TURKEY_HAVALEH', 'USD_AUSTRALIA_HAVALEH', 'AED_NAGHDI', 'USD_DUBAI', 
			 'SEKKEH', 'CNY_HAVALEH', 'GEL_HAVALEH', 'TRL_HAVALEH', 'MYR_HAVALEH', 'USD_DASTURI', 'TALA_MAZANNEH', 
			 'USD_KAGHAZI', 'SEKKEH_KAGHAZI']

SuffixList = ['_TIMELIST', '_OPEN', '_MIN', '_MAX', '_CLOSE', '_CHANGE']




def InsertIntoTable(db_file, table_name, timep, openp, minp, maxp, closep, changep):
	try:
		connectionObject = sqlite3.connect(cwd + db_file + '.db')
		cursorObject = connectionObject.cursor()
		query = "INSERT INTO " + table_name + "(_TIMELIST, _OPEN, _MIN, _MAX, _CLOSE, _CHANGE) VALUES({}, {}, {}, {}, {}, {})".format("1", openp, minp, maxp, closep, changep)
		cursorObject.execute(query)
		connectionObject.commit()
		# cursorObject.close()
	except Exception as e:
		print 'Insert Error: '
		print e
	connectionObject.close()


def CreateDatabase(db_file):
	connectionObject = sqlite3.connect(cwd + db_file + '.db')
	cursorObject = connectionObject.cursor()
	for i in PairsList:
		createTable = "CREATE TABLE " + i + "(id integer primary key autoincrement)"
		cursorObject.execute(createTable)
		for j in SuffixList:
			addColumn = "ALTER TABLE " + i +  " ADD COLUMN " + j + " text"
			cursorObject.execute(addColumn)
	connectionObject.close()

class Price:
    def __init__(self, pair, timeP, openP, minP, maxP, closeP, diffP = 0 ):
    	self.pair = pair
    	self.timeP = timeP
    	self.openP = openP
    	self.closeP = closeP
    	self.minP = minP
    	self.maxP = maxP
    	self.diffP = round(float((float(self.maxP) - float(self.minP))/float(self.minP)) * 100, 2)

    def Printer(self):
    	print '-'*(len(self.pair) + 7)
    	print 'Pair : ' +  str(self.pair)
    	print '-'*(len(self.pair) + 7)
    	print 'Time: ' + str(self.timeP)
    	print 'Open : ' + str(self.openP)
    	print 'Min : ' + str(self.minP)
    	print 'Max : ' + str(self.maxP)
    	print 'Close: ' + str(self.closeP)
    	if self.diffP > 0 :
    		print 'Change : + %' +  str(self.diffP)
    	else:
    		print 'Change : - %' +  str(self.diffP)
    	print '\n\n'


# g = globals()
# for i in PairsList:
#     for j in SuffixList:
#         g[i + '{0}'.format(j)] = []


flag = True
CreateDatabase('Currency')
while flag:
	page = requests.get('http://sabzemeydan.com')
	tree = html.fromstring(page.content)

	for i in tree.xpath('//td[@class = "text-center"]/text()'):
	    AllPriceList.append((i.replace(" ", '')).replace("\n", ""))

	for i in tree.xpath('//font[@color = "red"]/text()'):
	    ClosePriceList.append((i.replace(" ", '')).replace("\n", ""))
	try:
		k = 0
		j = 0
		for i in PairsList:
			PairX = Price(i, AllPriceList[k], AllPriceList[k + 1], AllPriceList[k + 2], AllPriceList[k + 3], ClosePriceList[j])
			# PairX.Printer()
			InsertIntoTable('Currency', i, PairX.timeP, PairX.openP, PairX.minP, PairX.maxP, PairX.closeP, PairX.diffP )

			# g[i + '_TIMELIST'].append(PairX.time)
			# g[i + '_OPEN'].append(PairX.openP)
			# g[i + '_CLOSE'].append(PairX.closeP)
			# g[i + '_MIN'].append(PairX.minP)
			# g[i + '_MAX'].append(PairX.maxP)
			k = k + 5
			j = j + 1
	except Exception as e:
		print e
		
	# for i in USD_NAGHDI_CLOSE:
	# 	print i
	# print '\n'


	connectionObject = sqlite3.connect(cwd + 'Currency.db')
	cursorObject = connectionObject.cursor()
	query = "SELECT * FROM USD_NAGHDI"
	o = cursorObject.execute(query)
	rows = o.fetchall()
	for i in rows:
		print i
	print  '\n\n'
	connectionObject.close()

	time.sleep(5)














