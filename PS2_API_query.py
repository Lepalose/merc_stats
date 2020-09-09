

#import json
#import sys
import urllib.request


# PS2 API to aquire MERC general stats
def ps2_qry(qry, stid=""):
	
	if stid != "":
		stid= "s:" + stid + "/"

	with urllib.request.urlopen("https://census.daybreakgames.com/"+stid+"get/ps2:v2/"+qry) as res:
		#data = json.loads(res.read().decode())
		data = res.read().decode()

	return data



#
#with urllib.request.urlopen("https://census.daybreakgames.com/s:mercstats/get/ps2:v2/outfit/?outfit_id=37509488620601577&c:resolve=member_character(name,type,faction)&c:resolve=member_online_status") as apiurl:
#    merc_data = json.loads(apiurl.read().decode())
    #print(merc_data)
    #print (json.dumps(merc_data, indent=5, sort_keys=True))
    #print(merc_data["outfit_list"][0]["members"][0]["character_id"])
    #print([mdata["character_id"] for mdata in merc_data["outfit_list"][0]["members"]])

# Acquire all character id's
#merc_charids = [mdata["character_id"] for mdata in merc_data["outfit_list"][0]["members"]]
#

#http://census.daybreakgames.com/get/ps2:v2/outfit?c:join=outfit_member^list:1^show:character_id^inject_at:members(characters_weapon_stat_by_faction^terms:stat_name=weapon_kills^list:1^on:character_id^to:character_id^show:value_nc'value_tr'value_vs'item_id'stat_name^inject_at:kills(item^on:item_id^show:item_category_id^outer:0^terms:item_category_id=9'item_category_id=10'item_category_id=20'item_category_id=21'item_category_id=22'item_category_id=23'item_id=1082'item_id=1083'item_id=1084^list:1))&c:lang=en&c:limit=20000&outfit_id=37528378292063884