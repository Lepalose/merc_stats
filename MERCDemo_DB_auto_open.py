#DATABASE QUERYING TEST

import glob


import json

import ast  #Needed for single quote loading of bad json data (outfit char list via MERC_OP_TRACKER.py)


import datetime
import pytz

import sys
import os

import PS2_API_query

import MERCDemo_OPS_UPLOAD
import MERCDemo_OP_PARSER


#DB START - END DATES
#START: 2017-04-26
#END: TODAY

#Manual day entry for auto-retry
dstart = datetime.datetime(2020,8,28)
dend = datetime.datetime(2020,8,28)
#dend = datetime.datetime.now()


def daterange(date1, date2):
	for n in range(int ((date2 - date1).days)+1):
		yield date1 + datetime.timedelta(n)


for dt in daterange(dstart, dend):
	#print(dt.strftime("%Y-%m-%d"))
	if dt.weekday() in (2, 4):
		print("Wednesday or Friday: ", dt.strftime("%Y-%m-%d"))	
		try:
			MERCDemo_OP_PARSER.parse_raw_ops_data(dt)
		except Exception as e:
			print("##### UPDATE FAIL: " + dt.strftime("%Y-%m-%d") + "#####")
			print(str(e))


		#dbpath = ".\MERC_OPS_data\\" + dt.strftime("%Y-%m-%d") + "\\"
		#filelist=glob.glob(dbpath + "*.json")
		#print(filelist[0])

		#for file in filelist:
		#	print(file)
		#	with open(file) as opdataf:
		#		k=0



#print(dstart)
#print(dend)


#FOR EACH DATA FILE ON THAT DATE:
#dbdate = "2017-08-04"
#dboutfit = "2017-08-04_characters"
#dbname = "0_2017-08-04_175609.json"


#dbpath = "./MERC_OPS_data/" + dbdate + "/"
#print(dbpath+dboutfit)
#print(dbpath+dbname)

#with open(dbpath+dbname) as opdataf: