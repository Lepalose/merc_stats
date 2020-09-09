import json

import ast  #Needed for single quote loading of bad json data (outfit char list via MERC_OP_TRACKER.py)


import datetime
import pytz

import sys
import os
import glob

import PS2_API_query

import MERCDemo_OPS_UPLOAD




###########################################
#   
#   PARSING OF EXISTING DATABASE
#   
###########################################

# Search Main Program for the primary routine below





# PLAYER & THEIR OUTFIT_ID LOOKUP:
def playerlookup (character_id):
	
	#STAT ID for API queries
	dbgstatid="mercstats"
	
	#Character lookup for faction / name
	qrybase="character/?character_id="
	qry=qrybase+character_id
	qry_res=PS2_API_query.ps2_qry(qry, dbgstatid)
	qry_res = json.loads(qry_res)
	try:
		char_res = {
			"character_id": character_id,
			"name": qry_res["character_list"][0]['name']['first'],
			"name_lower": qry_res["character_list"][0]['name']['first_lower'],
			"faction_id": qry_res["character_list"][0]['faction_id']
		}
	except:
		char_res = {
			"character_id": character_id,
			"name": 'UNKNOWN',
			"name_lower": 'unknown',
			"faction_id": '-5'
		}

	#Lookup for outfit
	qrybase2='outfit_member?character_id='
	qry2=qrybase2+character_id
	qry_res2=PS2_API_query.ps2_qry(qry2, dbgstatid)
	qry_res2 = json.loads(qry_res2)
	#char_res["outfit_id"] = qry_res2["outfit_member_list"][0]["outfit_id"]
	
	try:
		char_res["outfit_id"] = qry_res2["outfit_member_list"][0]["outfit_id"]
	except:
		#print('#### NO OUTFIT, FACTION: ', char_res['faction_id'])
		if char_res['faction_id'] == '1':
			char_res["outfit_id"] = '-1'
		elif char_res['faction_id'] == '2':
			char_res["outfit_id"] = '-2'
		elif char_res['faction_id'] == '3':
			char_res["outfit_id"] = '-3'
		else:
			char_res["outfit_id"] = '-5'

	return (char_res)


# OUTFIT DETAILS LOOKUP:
def outfitlookup (outfit_id):
	
	#STAT ID for API queries
	dbgstatid="mercstats"
	
	#Character lookup for faction / name
	qrybase="outfit/?outfit_id="
	qrypost="&c:resolve=leader(faction_id)"
	qry=qrybase+outfit_id+qrypost
	qry_res=PS2_API_query.ps2_qry(qry, dbgstatid)
	qry_res = json.loads(qry_res)


	try:
		out_res = {
		"outfit_id": outfit_id,
		"name": qry_res["outfit_list"][0]['name'],
		"name_lower": qry_res["outfit_list"][0]['name_lower'],
		"alias": qry_res["outfit_list"][0]['alias'],
		"alias_lower": qry_res["outfit_list"][0]['alias_lower'],
		"faction_id": qry_res["outfit_list"][0]['leader']['faction_id']
		}
	except:
		#print('#### NO OUTFIT: ', outfit_id)
		out_res = {
			'outfit_id': outfit_id
		}
		if outfit_id == '-1':
			out_res = {
				"outfit_id": outfit_id,
				"name": "VS - No Outfit",
				"name_lower": "vs - no outfit",
				"alias": "",
				"alias_lower": "",
				"faction_id": "1"
			}
		elif outfit_id == '-2':
			out_res = {
				"outfit_id": outfit_id,
				"name": "NC - No Outfit",
				"name_lower": "nc - no outfit",
				"alias": "",
				"alias_lower": "",
				"faction_id": "2"
			}
		elif outfit_id == '-3':
			out_res = {
				"outfit_id": outfit_id,
				"name": "TR - No Outfit",
				"name_lower": "tr - no outfit",
				"alias": "",
				"alias_lower": "",
				"faction_id": "3"
			}
		else:
			out_res = {
				"outfit_id": outfit_id,
				"name": "Other - No Outfit",
				"name_lower": "other - no outfit",
				"alias": "",
				"alias_lower": "",
				"faction_id": "5"
			}
	return (out_res)









# MAIN PROGRAM

def parse_raw_ops_data (parse_date):
	


	deathevents = []
	xpevents = []
	loginoutevents = []
	char_ids = set()
	char_info = []
	outfit_ids = set()
	outfit_info = []


	#DEFINING MERC OUTFIT CHARACTERS...
	outmem_list = set()
	dbgstatid="mercstats"
	target_out_id = "37509488620601577"
	qrybase = "outfit/?outfit_id="
	qryextra = "&c:resolve=member_character"
	qry=qrybase+target_out_id+qryextra
	qry_res=PS2_API_query.ps2_qry(qry, dbgstatid)
	qry_res = json.loads(qry_res)
	#print(qry_res)
	for out in qry_res["outfit_list"]:
		for out_mem in out["members"]:
			outmem_list.add(out_mem['character_id'])


	#FOR EACH DATA FILE ON THAT DATE:
	dbpath = ".\MERC_OPS_data\\" + parse_date.strftime("%Y-%m-%d") + "\\"
	filelist=glob.glob(dbpath + "*.json")
	#print(filelist[0])
	for file in filelist:
		print(file)
		with open(file) as opdataf:
			k=0
			for dataline in opdataf:
				jsdataline = json.loads(dataline)


				#GAIN EXPERIENCE EVENTS (most common)
				#Note:
				#Recording all events, but saving only MERC character_id values for character lookups
				#This means that I am not storing info about non-MERC rezzes/vehicle destructions
				#That is no info about the character who rezzed or got rezzed by a MERC character
				#or no info about the character who destroyed or got destroyed by a MERC character
				#These values can be added to the DB at a later date if needed
				
				if jsdataline["payload"]["event_name"] == "GainExperience":
					#MJG LIMITING FOR TESTING PURPOSES
					#k += 1
					#if k>50:
					#	break
					
					jsdataline=jsdataline["payload"]

					''' IGNORING GAIN XP '''
					if jsdataline["character_id"] in outmem_list:
						#print(jsdataline["character_id"] )
						char_ids.add(jsdataline["character_id"])
					#Not entirely sure what "other_id" is, sometimes it is a character id, sometimes something else
					#char_ids.add(jsdataline["other_id"])
					#note I am not adding all characters from gain XP events


					xpevents.append(jsdataline)
					


				#DEATH EVENT (2nd most common)
				elif jsdataline["payload"]["event_name"] == "Death":
					
					jsdataline=jsdataline["payload"]
					''' IGNORING DEATHS'''
					char_ids.add(jsdataline["character_id"])
					char_ids.add(jsdataline["attacker_character_id"])
					deathevents.append(jsdataline)
					
				
				elif jsdataline["payload"]["event_name"] == "PlayerLogout":
					#MJG LIMITING FOR TESTING PURPOSES
					#k += 1
					#if k>5:
				#		break
					jsdataline=jsdataline["payload"]

					#Assigning new dataline value (0 = logout event)
					jsdataline["loginout"] = 0 
					char_ids.add(jsdataline["character_id"])
					loginoutevents.append(jsdataline)		

				elif jsdataline["payload"]["event_name"] == "PlayerLogin":			

					jsdataline=jsdataline["payload"]

					#Assigning new dataline value (1 = login event)
					jsdataline["loginout"] = 1 
					char_ids.add(jsdataline["character_id"])
					loginoutevents.append(jsdataline)		



			#print(char_ids)
			#print(deathevents)


	# AFTER ALL DEATH EVENTS LOADED
	# API lookups for characters
	out_ids = set()
	chardata = []
	for char in char_ids:
		#print("".join(list(char)))
		print("Char_id: " + char)
		
		attempts=0
		while attempts < 10:
			try:
				chardata=playerlookup ("".join(list(char)))
				break
			except Exception as e:
				print("##### PS2 API LOOKUP FAIL #####")
				print(e)
				attempts += 1



		char_info.append(chardata)
		#print(chardata)
		out_ids.add(chardata["outfit_id"])

	# API lookups for outfits
	outfitdata = []
	for outfit in out_ids:
		print("Outfit ID: " + outfit)

		attempts=0
		while attempts < 10:
			try:
				outfitdata=outfitlookup ("".join(list(outfit)))
				break
			except Exception as e:
				print("##### PS2 API LOOKUP FAIL #####")
				print(e)
				attempts += 1
		outfit_info.append(outfitdata)
		#print(outfitdata)


	# CONNECT TO MERC SQL & UPDATE
	#LOCAL TESTING
	
	conn_info = {
		"host": "localhost",
		"port": 3306,
		"user": "testadm",
		"passwd": "test_all_the_things",
		"db": "mercadm_stats"
	}
	

	
	print("##### CONNECTING TO MYSQL #####")
	try: 
		MERCDemo_OPS_UPLOAD.ps2_ops_update (conn_info, parse_date.strftime("%Y-%m-%d"), xpevents, deathevents, loginoutevents, char_info, outfit_info)
	except Exception as e:
		print("##### DB UPDATE FAIL #####")
		print(str(e))



#parse_raw_ops_data(1)