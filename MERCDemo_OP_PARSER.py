import json

import ast  #Needed for single quote loading of bad json data (outfit char list via MERC_OP_TRACKER.py)


import datetime
from numpy import character, int64
import pytz

import sys
import os
import glob

#used to convert JSON into DataFrames, similar to in-memory DB's
import pandas as pd

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
	# print(qry)
	qry_res=PS2_API_query.ps2_qry(qry, dbgstatid)
	print(qry_res)
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

	return char_res


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
	return out_res









# MAIN PROGRAM

def parse_raw_ops_data (parse_date, your_outfit_id, other_outfit_ids=None):

	pd.options.display.float_format = '{:.0f}'.format

	#DEFINING MERC OUTFIT CHARACTERS...
	your_outfit_members = set()
	dbgstatid="mercstats"
	qrybase = "outfit/?outfit_id="
	resolve_member_characters = "&c:resolve=member_character"
	qry=qrybase + your_outfit_id + resolve_member_characters
	qry_res=PS2_API_query.ps2_qry(qry, dbgstatid)
	qry_res = json.loads(qry_res)
	#print(qry_res)
	for out in qry_res["outfit_list"]:
		for out_mem in out["members"]:
			your_outfit_members.add(out_mem['character_id'])


	#FOR EACH DATA FILE ON THAT DATE:
	dbpath = ".\MERC_OPS_data\\" + parse_date.strftime("%Y-%m-%d") + "\\"
	filelist=glob.glob(dbpath + "*.json")
	#print(filelist[0])

	json_datas = []

	for file in filelist:
		# print(file)
		json_datas.append(pd.read_json(file, orient='records', dtype=str))
	
	#has raw data that we received from websocket, now we join with new sets of data, like outfit, faction, etc
	json_dataframe = pd.concat(json_datas)

	#################################
	#STEP 1: get gain experience events; character_id is character that gained xp, if other_id != 0, then kill
	#################################

	gain_experience = json_dataframe.loc[json_dataframe['event_name'] == 'GainExperience']

	#only concerned about your outfit's gained experience, anything that isn't your outfit would be your outfit member dying
	your_outfit_gain_experience = gain_experience.loc[gain_experience['character_id'].isin(your_outfit_members)]

	your_outfit_gain_experience_dataframe = gain_experience[['timestamp', 'character_id', 'experience_id', 'amount', 'loadout_id', 'other_id', 'world_id', 'zone_id']]
	your_outfit_gain_experience_dataframe.rename(mapper={'timestamp': 'time_stamp'}, inplace=True)
	your_outfit_gain_experience_dataframe['time_stamp'] = your_outfit_gain_experience_dataframe['timestamp']
	your_outfit_gain_experience_dataframe.drop(labels=['timestamp'], axis=1, inplace=True)

	# your_outfit_gain_experience_dataframe['index'] = your_outfit_gain_experience_dataframe.reset_index().index

	char_data = []
	# for char_id in gain_experience['other_id'].unique():
	# 	print(str(char_id))
	# 	player_outfit_data = playerlookup(str(char_id))
	# 	char_data.append(player_outfit_data)

	for char_id in your_outfit_gain_experience['character_id'].unique():
		player_outfit_data = playerlookup(str(char_id))
		char_data.append(player_outfit_data)
	

	# player_outfit_data = playerlookup('5428010618038207793')
	# outfit_data.append(player_outfit_data)

	char_data = pd.DataFrame(char_data, dtype=str)

	outfit_data = []
	for outfit_id in char_data['outfit_id'].unique():
		cur_outfit_data = outfitlookup(outfit_id)
		outfit_data.append(cur_outfit_data)
	
	#char_id, name, name_lower, facction_id, outfit_id
	outfit_data = pd.DataFrame(outfit_data, dtype=str)
	outfit_data['op_date'] = parse_date.strftime("%Y-%m-%d")

	#################################
	#STEP 2: get deaths; other_id is character that killed, character_id is character that was killed
	#################################

	deaths = json_dataframe.loc[json_dataframe['event_name'] == 'Death']

	your_outfit_deaths_dataframe = deaths.loc[deaths['character_id'].isin(your_outfit_members)]
	your_outfit_deaths_dataframe['time_stamp'] = your_outfit_deaths_dataframe['timestamp']
	your_outfit_deaths_dataframe.drop(labels=['amount', 'event_name', 'experience_id', 'loadout_id', 'other_id', 'facility_id', 'outfit_id', 'timestamp', 'faction_id', 'vehicle_id'], axis=1, inplace=True)

	#################################
	#STEP 3: get logouts
	#################################

	logouts = json_dataframe.loc[json_dataframe['event_name'] == 'PlayerLogout']

	your_outfit_logouts = logouts.loc[logouts['character_id'].isin(your_outfit_members)]

	#################################
	#STEP 4: get logins
	#################################

	#loginouts table prepared
	logins = json_dataframe.loc[json_dataframe['event_name'] == 'PlayerLogin']

	your_outfit_logins = logins.loc[logins['character_id'].isin(your_outfit_members)]

	your_outfit_loginouts = pd.concat([your_outfit_logouts, your_outfit_logins])

	your_outfit_loginouts.rename(mapper={'event_name': 'loginout'}, axis=1, inplace=True)

	# print(your_outfit_loginouts.columns)

	your_outfit_loginouts = your_outfit_loginouts.replace(to_replace={'loginout': 'PlayerLogout'}, value=0, inplace=False)

	your_outfit_loginouts = your_outfit_loginouts.replace(to_replace={'loginout': 'PlayerLogin'}, value=1, inplace=False)

	your_outfit_loginouts['loginout'] = your_outfit_loginouts['loginout'].astype('bool')

	your_outfit_loginouts['time_stamp'] = your_outfit_loginouts['timestamp']

	your_outfit_loginouts_dataframe = your_outfit_loginouts[['time_stamp', 'character_id', 'loginout', 'world_id']]

	#char table prepared
	char_dataframe = char_data.drop('outfit_id', axis=1, inplace=False)
	# print(char_dataframe)

	#char_outfit table prepared
	char_outfit_dataframe = char_data.drop(labels=['name', 'name_lower', 'faction_id'], axis=1)
	char_outfit_dataframe['op_date'] = parse_date.strftime("%Y-%m-%d")

	#################################
	#STEP 4: get ps2_factions; IGNORING FOR NOW
	#################################

	# CONNECT TO MERC SQL & UPDATE
	#LOCAL TESTING
	
	conn_info = {
		"host": "localhost",
		"port": 3306,
		"user": "testadm",
		"passwd": "test_all_the_things",
		"db": "mercdemo"
	}
	

	
	print("##### CONNECTING TO MYSQL #####")
	try: 
		MERCDemo_OPS_UPLOAD.ps2_ops_update (conn_info, 
				parse_date.strftime("%Y-%m-%d"), 
				your_outfit_gain_experience_dataframe, 
				your_outfit_deaths_dataframe, 
				your_outfit_loginouts_dataframe, 
				char_dataframe, 
				char_outfit_dataframe,
				outfit_data)
	except Exception as e:
		print("##### DB UPDATE FAIL #####")
		print(str(e))



#parse_raw_ops_data(1)

if __name__ == "__main__":
	parse_date = datetime.datetime(year=2021, month=8, day=22, hour=22, minute=18, second=21)
	parse_raw_ops_data(parse_date, '37509488620601577')