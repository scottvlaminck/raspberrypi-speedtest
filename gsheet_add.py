import ConfigParser
import fileinput
import gdata.spreadsheets.client
import gdata.spreadsheets.data
import gdata.gauth
import os


# see: https://pythonhosted.org/gdata/docs/auth.html#docs-auth

# - https://developers.google.com/apps-script/guides/rest/api#general_procedure 
# - https://developers.google.com/apps-script/guides/rest/quickstart/python#step_1_turn_on_the_api_name 


config_filename = os.path.splitext(os.path.realpath(__file__))[0]+'.cfg'
config = ConfigParser.ConfigParser()
config.read(config_filename)


if not (config.has_option('oauth', 'client_id') and config.has_option('oauth', 'client_secret')):
	raise ValueError('auth client_id and client_secret are required')


client_id=config.get('oauth', 'client_id')
client_secret=config.get('oauth', 'client_secret')

access_token=config.get('oauth_token', 'access_token')
refresh_token=config.get('oauth_token', 'refresh_token')

sheet_id=config.get('sheet_info', 'sheet_id')
tab_id=config.get('sheet_info', 'tab_id')

connection_type=config.get('other_values', 'connection_type')




for result_string in fileinput.input():
	
	result_names = ['startdate', 'stopdate', 'provider', 'ip', 'speedtestserver', 'distance', 'pingtime', 'downloadspeed', 'uploadspeed', 'resultimg']
	
	# 2016-04-26 02:59:03;2016-04-26 02:59:37;CenturyLink;97.116.3.36;US Internet (Minnetonka, MN);16.21 km;45.778 ms;45.73 Mbit/s;16.96 Mbit/s;http://www.speedtest.net/result/5278910900.png
	result_list = result_string.split(";")
	
	
	# create the OAuth2 token
	token = gdata.gauth.OAuth2Token(client_id=client_id,client_secret=client_secret,scope='https://spreadsheets.google.com/feeds/',user_agent='rpi-speedtest-add',access_token=access_token,refresh_token=refresh_token)
	
	# create the spreadsheet client and authenticate
	spr_client = gdata.spreadsheets.client.SpreadsheetsClient()
	token.authorize(spr_client)
	
	#create a ListEntry. the first item of the list corresponds to the first 'header' row
	entry = gdata.spreadsheets.data.ListEntry()
	
	entry.set_value('connectiontype', connection_type)
	
	for i in range(len(result_list)):
		
		clean_result = result_list[i].strip()
		
		for ending in [" km", " ms", " Mbit/s"]: 		
			if clean_result.endswith(ending):
			    clean_result = clean_result[:-len(ending)]
			
		entry.set_value(result_names[i], clean_result)

	# add the ListEntry you just made
	spr_client.add_list_entry(entry, sheet_id, tab_id)

#	print ""
#	print entry
#	print ""


