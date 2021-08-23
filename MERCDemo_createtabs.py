import MySQLdb

#NOTE BEFORE RUNNING:
#XAMPP - MySQL Database needs to be created, then user with all privileges 
#Database: mercadm_stats
#Here >> User: testadm  password: tests_all_the_things

# CONNECTION TO DB
#FOR LOCAL TESTING
db=MySQLdb.connect(host="localhost", user="testadm", passwd="test_all_the_things", db="mercdemo")
print("CONNECTED TO LOCALHOST")

#Cursor object
cursor=db.cursor()
#using .basecursor (confirm) does not raise Warnings
print("MADE CURSOR")


# CREATE DEATH TABLE
# Suppress warnings
#cursor.execute("SET sql_notes = 0; ")
#cursor.execute("CREATE TABLE IF NOT EXISTS deathevents (email varchar(70),pwd varchar(20));")
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_death_events (id int(11) NOT NULL AUTO_INCREMENT, time_stamp int(10), \
	character_id bigint(19), character_loadout_id int(11), attacker_character_id bigint(19), attacker_fire_mode_id int(11), \
	attacker_loadout_id int(11), attacker_weapon_id int(11), attacker_vehicle_id int(11), is_headshot boolean NOT NULL DEFAULT 0, \
	world_id int(11), zone_id int(11), PRIMARY KEY (id));")

print("MADE ps2_death_events")


#CREATE CHARACTER TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_char (character_id bigint(19), name varchar(70), name_lower varchar(70), faction_id int(11), PRIMARY KEY (character_id));")
print("MADE ps2_char")


#CREATE CHAR-OUTFIT TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_char_outfit (op_date date, character_id bigint(19), outfit_id bigint(19), PRIMARY KEY (op_date, character_id));")
print("MADE ps2_char_outfit")


#CREATE OUTFIT TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_outfit (op_date date, outfit_id bigint(19), name varchar(70), name_lower varchar(70), alias varchar(4), \
	alias_lower varchar(4), faction_id int(11), PRIMARY KEY (op_date, outfit_id));")
print("MADE ps2_outfit")


#CREATE FACTIONS TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_faction (faction_id int(11), faction_name varchar(70), faction_abbrv varchar(4), PRIMARY KEY (faction_id));")
print("MADE ps2_faction")


# CREATE GAINXP TABLE
#cursor.execute("CREATE TABLE IF NOT EXISTS deathevents (email varchar(70),pwd varchar(20));")
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_gainxp_events (id int(11) NOT NULL AUTO_INCREMENT, time_stamp int(10), \
    character_id bigint(19), experience_id int(11), amount int(11), loadout_id int(11), \
    other_id bigint(19), world_id int(11), zone_id int(11), PRIMARY KEY (id));")
print("MADE ps2_gainxp_events")


# CREATE LOGINOUT TABLE
#cursor.execute("CREATE TABLE IF NOT EXISTS deathevents (email varchar(70),pwd varchar(20));")
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_loginout_events (time_stamp int(10), \
    character_id bigint(19), loginout boolean NOT NULL DEFAULT 0, world_id int(11), PRIMARY KEY (time_stamp, character_id));")
print("MADE ps2_loginout_events")


#2018-02-15 UPDATE
# CREATE XP LIST TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_xplist (experience_id int(10), \
    description varchar(70), xp int(10), category int(10) DEFAULT 0, PRIMARY KEY (experience_id));")
print("MADE ps2_xplist")


#2018-03-27 UPDATE
# CREATE AVG/MAX LIST TABLE
cursor.execute("CREATE TABLE IF NOT EXISTS ps2_avgmax_list (char_or_outfit_id bigint(19), \
    num_ops int(10) DEFAULT 0, kill_max int(10) DEFAULT 0, kill_avg int(10) DEFAULT 0, \
    death_max int(10) DEFAULT 0, death_avg int(10) DEFAULT 0, \
    xp_max int(10) DEFAULT 0, xp_avg int(10) DEFAULT 0, \
    PRIMARY KEY (char_or_outfit_id));")
cursor.execute("INSERT INTO ps2_avgmax_list (char_or_outfit_id) VALUES(37509488620601577)")
print("MADE ps2_avgmax_list")


# Reactivate warnings
#cursor.execute("SET sql_notes = 1; ")

# INSERT DATA INTO TABLE
# Note: data must be in tuples
#cursor.execute("INSERT INTO testtab (email,pwd) VALUES('test@gmail.com','test')")


# Commit your changes in the database
db.commit()
print("CHANGES COMMITTED")


# disconnect from mysql server
db.close()
print("DB CLOSED")
print("SERVER STOPPED")