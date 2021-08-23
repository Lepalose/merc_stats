# import MySQLdb
import datetime
import pymysql
from sqlalchemy import create_engine
import pandas as pd

###########################################
#   
#   PS2 OP DATA UPLOAD TO SQL 
#   
###########################################


#Tables:
#ps2_gainxp_events
#ps2_death_events
#ps2_char
#ps2_char_outfit
#ps2_outfit
#ps2_faction

#table names:
ps2_char = 'ps2_char'
ps2_char_outfit = 'ps2_char_outfit'
ps2_outfit = 'ps2_outfit'
ps2_faction = 'ps2_faction'
ps2_gainxp_events = 'ps2_gainxp_events'
ps2_loginout_events = 'ps2_loginout_events'
ps2_death_events = 'ps2_death_events'


#UPDATE GAIN XP EVENTS TABLE
def t_gainxp_up(xpevents, db):

	xp_up=[]
	#FOR EACH LINE
	for gxp in xpevents:
		#For executemay approach:
		xp_up.append((
			gxp["timestamp"],
			gxp["character_id"],
			gxp["experience_id"],
			gxp["amount"],
			gxp["loadout_id"],
			gxp["other_id"],
			gxp["world_id"],
			gxp["zone_id"]
			))
	# INSERT DATA INTO ps2_gainxp_events TABLE
	sqlinput = ("""REPLACE INTO ps2_gainxp_events (time_stamp, character_id, experience_id, """
			"""amount, loadout_id, other_id, world_id, zone_id) """
			"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")
	#print(sqlinput)

	#Cursor object
	cursor=db.cursor()

	try:
		cursor.executemany(sqlinput,xp_up)
		db.commit()
	except Exception as e:
		print("##### ps2_gainxp_events: Execute Many FAIL #####")
		print(str(e))
		db.rollback()






#UPDATE DEATH EVENTS TABLE
def t_death_up(deathevents, db):
	
	dth_up = []
	#FOR EACH LINE
	for dth in deathevents:
		#For executemay approach:
		dth_up.append((
			dth["timestamp"],
			dth["character_id"],
			dth["character_loadout_id"],
			dth["attacker_character_id"],
			dth["attacker_fire_mode_id"],
			dth["attacker_loadout_id"],
			dth["attacker_weapon_id"],
			dth["attacker_vehicle_id"], 
			dth["is_headshot"],
			dth["world_id"],
			dth["zone_id"]
			))

	# INSERT DATA INTO ps2_death_events TABLE
	sqlinput = ("""REPLACE INTO ps2_death_events (time_stamp, character_id, character_loadout_id, """
			"""attacker_character_id, attacker_fire_mode_id, attacker_loadout_id, attacker_weapon_id, attacker_vehicle_id, """
			"""is_headshot, world_id, zone_id) """
			"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
	#print(sqlinput)

	#Cursor object
	cursor=db.cursor()

	try:
		cursor.executemany(sqlinput,dth_up)
		db.commit()
	except Exception as e:
		print("##### ps2_death_events: Execute Many FAIL #####")
		print(str(e))
		db.rollback()







#UPDATE LOGIN/OUT EVENTS TABLE
def t_loginout_up(loginoutevents, db):

	loginout_up=[]
	#FOR EACH LINE
	for loginout in loginoutevents:
		#For executemay approach:
		loginout_up.append((
			loginout["timestamp"],
			loginout["character_id"],
			loginout["loginout"],
			loginout["world_id"]
			))
	# INSERT DATA INTO ps2_gainxp_events TABLE
	sqlinput = ("""REPLACE INTO ps2_loginout_events (time_stamp, character_id, loginout, world_id) """
			"""VALUES (%s, %s, %s, %s)""")
	#print(sqlinput)

	#Cursor object
	cursor=db.cursor()

	try:
		cursor.executemany(sqlinput,loginout_up)
		db.commit()
	except Exception as e:
		print("##### ps2_gainxp_events: Execute Many FAIL #####")
		print(str(e))
		db.rollback()













#UPDATE CHARACTER & CHARACTER_OUTFIT TABLES
def t_char_t_charout_up(charlist, opdate, db):
	
	#cursor.execute("SET sql_notes = 0; ")
	#FOR EACH LINE
	char_up = [] 
	char_out_up = []
	for char in charlist:
		#Create list of items for SQL
		char_up.append((
			char["character_id"],
			char["name"],
			char["name_lower"],
			char["faction_id"]
			))
		char_out_up.append((
			opdate,
			char["character_id"],
			char["outfit_id"],
			))

	# INSERT DATA INTO ps2_char TABLE
	# Note: data must be in tuples
	#print(rowvals)
	sqlinput = ("""REPLACE INTO ps2_char (character_id, name, name_lower, faction_id) """
		"""VALUES (%s, %s, %s, %s)""")
	print(sqlinput)


	#Cursor object
	cursor=db.cursor()
	try:
		cursor.executemany(sqlinput,char_up)
		db.commit()
	except Exception as e:
		print("##### ps2_char: Execute Many FAIL #####")
		print(str(e))
		db.rollback()

	#INSERT INTO ps2_char_outfit TABLE
	sqlinput = ("""REPLACE INTO ps2_char_outfit (op_date, character_id, outfit_id) """
		"""VALUES (%s, %s, %s)""")
	print(sqlinput)
	
	#Cursor object
	cursor=db.cursor()
	try:
		cursor.executemany(sqlinput,char_out_up)
		db.commit()
	except Exception as e:
		print("##### ps2_char_outfit: Execute Many FAIL #####")
		print(str(e))
		db.rollback()




#UPDATE OUTFIT TABLE
def t_outfit_up(opdate, outfitlist, db):
	
	#cursor.execute("SET sql_notes = 0; ")
	
	outfit_up = []
	#FOR EACH LINE
	for outfit in outfitlist:
		#Create list of items for SQL
		outfit_up.append((
			opdate,
			outfit["outfit_id"],
			outfit["name"],
			outfit["name_lower"],
			outfit["alias"],
			outfit["alias_lower"],
			outfit["faction_id"],
			))
 
	# INSERT DATA INTO TABLE
	# Note: data must be in tuples
	#print(rowvals)
	sqlinput = ("""REPLACE INTO ps2_outfit (op_date, outfit_id, name, name_lower, alias, alias_lower, faction_id) """
		"""VALUES (%s, %s, %s, %s, %s, %s, %s)""")
	print(sqlinput)
	
	#Cursor object
	cursor=db.cursor()
	try:
		cursor.executemany(sqlinput,outfit_up)
		db.commit()
	except Exception as e:
		print("##### ps2_outfit: Execute Many FAIL #####")
		print(str(e))
		db.rollback()










def t_avgmax_up(opdate, srch_outfit, db):

	def incrAvg (old_avg, new_count, new_sample):
		return old_avg + ((new_sample - old_avg) / new_count)

	
	
	cursor = db.cursor()

	error = ""

	#Get current count / avg / max data
	sqlsearch = ("""SELECT * FROM ps2_avgmax_list""")
	try:
		# Execute the SQL command
		cursor.execute(sqlsearch)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		#print(results)
		avgmax={}
		for row in results:
			# Now print fetched result
			#print (row)
			avgmax[str(row[0])] = {}
			avgmax[str(row[0])]["count"] = row[1]
			avgmax[str(row[0])]["kill_max"] = row[2]
			avgmax[str(row[0])]["kill_avg"] = row[3]
			avgmax[str(row[0])]["death_max"] = row[4]
			avgmax[str(row[0])]["death_avg"] = row[5]
			avgmax[str(row[0])]["xp_max"] = row[6]
			avgmax[str(row[0])]["xp_avg"] = row[7]

			#print(avgmax[str(row[0])]["count"])
	except:
		new_error = "Error: unable to fecth data on COUNT/AVG/MAX SEARCH"
		print (new_error)
		error = '\n'.join([error, new_error])
	
	#print (avgmax)



	#FINDING OP KILL/DEATH VALUES
	
	sqlsearch = """
	SELECT *
	FROM
	(    SELECT mercm.character_id, mercm.name, 
			SUM(1) AS tot_d, #CHECKING FO TOTAL DEATHS OF ALL INCLUDING DELETED CHARS i.e., faction -5 which may be suicides?
			SUM(CASE WHEN att.faction_id=1 OR att.faction_id=2 OR att.faction_id=3 THEN 1 ELSE 0 END) AS meas_d,
			SUM(CASE WHEN att.faction_id=1 THEN 1 ELSE 0 END) AS vs_d,
			SUM(CASE WHEN att.faction_id=2 THEN 1 ELSE 0 END) AS nc_d,
			SUM(CASE WHEN att.faction_id=3 AND adth.character_id != adth.attacker_character_id THEN 1 ELSE 0 END) AS tr_d,
			SUM(CASE WHEN att.faction_id=3 AND att_charout.outfit_id = """ + srch_outfit + """ AND adth.character_id != adth.attacker_character_id THEN 1 ELSE 0 END) AS merc_d,
			SUM(CASE WHEN adth.character_id = adth.attacker_character_id THEN 1 ELSE 0 END) AS suicd

		FROM ps2_char_outfit
		INNER JOIN ps2_char AS mercm ON ps2_char_outfit.character_id = mercm.character_id
		INNER JOIN ps2_death_events AS adth ON adth.character_id = mercm.character_id AND from_unixtime(adth.time_stamp, '%Y-%m-%d') = '""" + opdate + """'
		INNER JOIN ps2_char AS att ON att.character_id = adth.attacker_character_id
		LEFT JOIN ps2_char_outfit AS att_charout ON att.character_id = att_charout.character_id AND att_charout.op_date = '""" + opdate + """'
		WHERE ps2_char_outfit.op_date = '""" + opdate + """' AND ps2_char_outfit.outfit_id = """ + srch_outfit + """
		GROUP BY mercm.character_id
	) AS DT
	JOIN 
		(
		SELECT mercm.character_id, mercm.name, 
			SUM(1) AS tot_k, #CHECKING FO TOTAL DEATHS OF ALL INCLUDING DELETED CHARS i.e., faction -5 which may be suicides?
			SUM(CASE WHEN vic.faction_id=1 OR vic.faction_id=2 THEN 1 ELSE 0 END) AS meas_k,
			SUM(CASE WHEN (vic.faction_id=1 OR vic.faction_id=2) AND is_headshot=1 THEN 1 ELSE 0 END) AS meas_hs,
			SUM(CASE WHEN vic.faction_id=1 THEN 1 ELSE 0 END) AS vs_k,
			SUM(CASE WHEN vic.faction_id=2 THEN 1 ELSE 0 END) AS nc_k, 
			SUM(CASE WHEN vic.faction_id=3 AND akill.character_id != akill.attacker_character_id THEN 1 ELSE 0 END) AS tr_k,
			SUM(CASE WHEN vic.faction_id=3 AND vic_charout.outfit_id = """ + srch_outfit + """ AND akill.character_id != akill.attacker_character_id THEN 1 ELSE 0 END) AS merc_k
			
		FROM ps2_char_outfit
		INNER JOIN ps2_char AS mercm ON ps2_char_outfit.character_id = mercm.character_id
		INNER JOIN ps2_death_events AS akill ON akill.attacker_character_id = mercm.character_id AND from_unixtime(akill.time_stamp, '%Y-%m-%d') = '""" + opdate + """'
		INNER JOIN ps2_char AS vic ON vic.character_id = akill.character_id
		LEFT JOIN ps2_char_outfit AS vic_charout ON vic.character_id = vic_charout.character_id AND vic_charout.op_date = '""" + opdate + """'
		WHERE ps2_char_outfit.op_date = '""" + opdate + """' AND ps2_char_outfit.outfit_id = """ + srch_outfit + """
		GROUP BY mercm.character_id
		) AS KT
	ON DT.character_id = KT.character_id
	"""

	try:
		# Execute the SQL command
		cursor.execute(sqlsearch)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		#print(results)
		char_kd={}
		op_deaths = 0
		op_kills = 0
		for row in results:
			# Now print fetched result
			#print (row)
			curr_char_id = str(row[0])
			char_kd[curr_char_id] = {}
			char_kd[curr_char_id]["deaths"] = row[3]
			op_deaths += row[3]
			char_kd[curr_char_id]["kills"] = row[12]
			op_kills += row[12]

			if curr_char_id not in avgmax:
				avgmax[curr_char_id] = {}
				avgmax[curr_char_id]["count"] = 0
				avgmax[curr_char_id]["kill_max"] = 0
				avgmax[curr_char_id]["kill_avg"] = 0
				avgmax[curr_char_id]["death_max"] = 0
				avgmax[curr_char_id]["death_avg"] = 0
				avgmax[curr_char_id]["xp_max"] = 0
				avgmax[curr_char_id]["xp_avg"] = 0


			avgmax[curr_char_id]["count"] += 1

			avgmax[curr_char_id]["kill_avg"] = incrAvg(avgmax[curr_char_id]["kill_avg"] , avgmax[curr_char_id]["count"], row[12])
			if row[12] > avgmax[curr_char_id]["kill_max"]:
				avgmax[curr_char_id]["kill_max"] = row[12]

			avgmax[curr_char_id]["death_avg"] = incrAvg(avgmax[curr_char_id]["death_avg"] , avgmax[curr_char_id]["count"], row[3])
			if row[3] > avgmax[curr_char_id]["death_max"]:
				avgmax[curr_char_id]["death_max"] = row[3]

			#print(avgmax[str(row[0])]["count"])

	except:
		new_error = "Error: unable to fecth/parse data of OP Kills/Death SEARCH"
		print (new_error)
		error = '\n'.join([error, new_error])

	





	#FINDING OP XP VALUES
	
	sqlsearch = ("""
		SELECT  xpchar.character_id AS xpcharacterid,
			SUM(ps2_gainxp_events.amount) AS xpamount

		FROM ps2_gainxp_events
		INNER JOIN ps2_char AS xpchar ON ps2_gainxp_events.character_id = xpchar.character_id
		INNER JOIN ps2_char_outfit AS xpchar_charout ON xpchar.character_id = xpchar_charout.character_id 
			AND xpchar_charout.op_date =  from_unixtime(ps2_gainxp_events.time_stamp, '%Y-%m-%d')
		INNER JOIN ps2_xplist as xplist ON ps2_gainxp_events.experience_id = xplist.experience_id
		WHERE (from_unixtime(ps2_gainxp_events.time_stamp, '%Y-%m-%d %h:%i:%s') 
			BETWEEN CONVERT_TZ('""" + opdate + """  06:00:00', 'US/Pacific', 'US/Eastern') 
				AND CONVERT_TZ('""" + opdate + """  09:00:00' , 'US/Pacific', 'US/Eastern')) 
				AND xpchar_charout.outfit_id = """ + srch_outfit + """
		GROUP BY xpchar.character_id
	""")


	try:
		# Execute the SQL command
		cursor.execute(sqlsearch)
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		#print("Pass fetchall")
		char_xp = {}
		op_xp = 0
		for row in results:
			# Now print fetched result
			#print (row)
			curr_char_id = str(row[0])
			char_xp[curr_char_id] = {}
			char_xp[curr_char_id]["xp"] = row[1]
			op_xp += row[1]
			#print(row)
			if curr_char_id not in avgmax:
				#print("New ID: " + curr_char_id)
				avgmax[curr_char_id] = {}
				avgmax[curr_char_id]["count"] = 1
				avgmax[curr_char_id]["kill_max"] = 0
				avgmax[curr_char_id]["kill_avg"] = 0
				avgmax[curr_char_id]["death_max"] = 0
				avgmax[curr_char_id]["death_avg"] = 0
				avgmax[curr_char_id]["xp_max"] = 0
				avgmax[curr_char_id]["xp_avg"] = 0
				#avgmax[curr_char_id]["count"] += 1
				#print("Done new ID")
			avgmax[curr_char_id]["xp_avg"] = incrAvg(avgmax[curr_char_id]["xp_avg"] , avgmax[curr_char_id]["count"], row[1])
			if row[1] > avgmax[curr_char_id]["xp_max"]:
				avgmax[curr_char_id]["xp_max"] = row[1]

	except Exception as e:
		new_error = "Error: unable to fecth/parse data of OP XP SEARCH"
		print (new_error)
		print (e)
		error = '\n'.join([error, new_error])
	
	#print(char_kd)
	#print(op_kills)
	#print(op_deaths)
	#print(op_xp)
	#print(avgmax)






	if op_kills != 0 or op_deaths != 0 or op_xp != 0 and error == "":

		
		avgmax[srch_outfit]["count"] += 1

		avgmax[srch_outfit]["kill_avg"] = incrAvg(avgmax[srch_outfit]["kill_avg"] , avgmax[srch_outfit]["count"], op_kills)
		if op_kills > avgmax[srch_outfit]["kill_max"]:
			avgmax[srch_outfit]["kill_max"] = op_kills


		avgmax[srch_outfit]["death_avg"] = incrAvg(avgmax[srch_outfit]["death_avg"] , avgmax[srch_outfit]["count"], op_deaths)
		if op_deaths > avgmax[srch_outfit]["death_max"]:
			avgmax[srch_outfit]["death_max"] = op_deaths

		
		avgmax[srch_outfit]["xp_avg"] = incrAvg(avgmax[srch_outfit]["xp_avg"] , avgmax[srch_outfit]["count"], op_xp)
		if op_xp > avgmax[srch_outfit]["xp_max"]:
			avgmax[srch_outfit]["xp_max"] = op_xp


		# INSERT DATA INTO ps2_gainxp_events TABLE
		sqlupdate = ("""REPLACE INTO ps2_avgmax_list (char_or_outfit_id, num_ops, kill_max, kill_avg, """
				"""death_max, death_avg, xp_max, xp_avg) """
				"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")

		avgmax_up = []
		for id_row in avgmax:
			#Create list of items for SQL
			#print(id_row)
			curr_char_id = str(id_row)
			avgmax_up.append((
				int(id_row),
				int(avgmax[curr_char_id]["count"]),
				int(avgmax[curr_char_id]["kill_max"]),
				int(avgmax[curr_char_id]["kill_avg"]),
				int(avgmax[curr_char_id]["death_max"]),
				int(avgmax[curr_char_id]["death_avg"]),
				int(avgmax[curr_char_id]["xp_max"]),
				int(avgmax[curr_char_id]["xp_avg"])
				))

		#print(avgmax_up)
		#Cursor object
		cursor=db.cursor()
		try:
			cursor.executemany(sqlupdate,avgmax_up)
			db.commit()
			print("##### AVERAGES & MAXES UPDATED FOR " + opdate + " #####")
		except Exception as e:
			print("##### ps2_outfit: Execute Many FAIL on AVG/MAX UPDATE #####")
			print(str(e))
			db.rollback()
	else:
		print("##### NOT UPDATING AVERAGES FOR " + opdate + " #####")






















# MAIN FUNCTION

def ps2_ops_update (conn_info, opdate, gain_xp_events, death_events, loginout_events, char_dataframe, char_outfit_dataframe, outfit_dataframe):

	pymysql.install_as_MySQLdb()

	#url needs to be encoded for special characters

	engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (conn_info['user'], conn_info['passwd'], conn_info['host'],  conn_info['port'], conn_info['db']))

	engine.connect()

	# CONNECTION TO DB
	# db=pymysql.connect(host=conn_info["host"], port=conn_info["port"], user=conn_info["user"], passwd=conn_info["passwd"], db=conn_info["db"])
	print("##### CONNECTED TO DATABASE #####")

	#UPDATING THE OP TABLES

	gain_xp_events.to_sql(ps2_gainxp_events, engine, if_exists='append', index=False)
	death_events.to_sql(ps2_death_events, engine, if_exists='append', index=False)
	loginout_events.to_sql(ps2_loginout_events, engine, if_exists='append', index=False)
	char_dataframe.to_sql(ps2_char, engine, if_exists='append', index=False)
	char_outfit_dataframe.to_sql(ps2_char_outfit, engine, if_exists='append', index=False)
	outfit_dataframe.to_sql(ps2_outfit, engine, if_exists='append', index=False)

	print('completed upload')
	
	# t_gainxp_up(xpevents, db)
	# t_death_up(deathevents, db)
	# t_loginout_up(loginoutevents, db)
	# t_char_t_charout_up(charlist, opdate, db)
	# t_outfit_up(opdate, outfitlist, db)

	db=pymysql.connect(host=conn_info["host"], port=conn_info["port"], user=conn_info["user"], passwd=conn_info["passwd"], db=conn_info["db"])
	
	srch_outfit = "37509488620601577"
	t_avgmax_up(opdate, srch_outfit, db)

	# disconnect from server
	engine.dispose()
	print("##### UPDATING FINISHED, CONNECTION CLOSED #####")


