import ConfigParser
import fileinput
import requests
import gdata.spreadsheets.client
import gdata.spreadsheets.data
import gdata.gauth
import os
from dateutil.parser import parse
from datetime import datetime, timedelta

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

def add_decimal_point(i):
	return i[:2] + '.' + i[2:] + ' '

for result_string in fileinput.input():
	
	result_names = ['startdate', 'stopdate', 'provider', 'ip', 'speedtestserver', 'distance', 'pingtime', 'downloadspeed', 'uploadspeed', 'resultimg', 'snrvalues']
	try:
		snr_values = requests.get("http://192.168.0.1/walk?oids=1.3.6.1.4.1.4491.2.1.20.1.24.1.1;&_n=80212&_=1498924016542").json().values()
		snr_values.remove('Finish')	
	except:
		snr_values = []		
		pass
	snr_decimalised = map(add_decimal_point, snr_values)
	snr_string = ','.join(snr_decimalised)

	if result_string.rst	ip() == 'error':
		log_file = open('error_log.txt','a')
		log_file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ';' + '\'' + snr_string + '\n')
		break

	# 2016-04-26 02:59:03;2016-04-26 02:59:37;CenturyLink;97.116.3.36;US Internet (Minnetonka, MN);16.21 km;45.778 ms;45.73 Mbit/s;16.96 Mbit/s;http://www.speedtest.net/result/5278910900.png
	result_list = result_string.split("\t")
	result_list.append('\'' + snr_string)

	# create the OAuth2 token
	token = gdata.gauth.OAuth2Token(client_id=client_id,client_secret=client_secret,scope='https://spreadsheets.google.com/feeds/',user_agent='rpi-speedtest-add',access_token=access_token,refresh_token=refresh_token)

	# create the spreadsheet client and authenticate
	spr_client = gdata.spreadsheets.client.SpreadsheetsClient()
	token.authorize(spr_client)

	log_file = open('error_log.txt','r')
	previous_errors = log_file.readlines()
	for error in previous_errors:
		error_list = error.split(';')
		entry = gdata.spreadsheets.data.ListEntry()
		entry.set_value('connectiontype', 'unavailable')
		entry.set_value('startdate', error_list[0])
		entry.set_value('snrvalues', error_list[1])
		spr_client.add_list_entry(entry, sheet_id, tab_id)

	#create a ListEntry. the first item of the list corresponds to the first 'header' row
	entry = gdata.spreadsheets.data.ListEntry()

	entry.set_value('connectiontype', connection_type)

	for i in range(len(result_list)):

		clean_result = result_list[i].strip()

		for ending in [" km", " ms", " Mbit/s"]:
			if clean_result.endswith(ending):
				clean_result = clean_result[:-len(ending)]

		print(result_names)
		print(clean_result)
		entry.set_value(result_names[i], clean_result)

	# add the ListEntry you just made
	spr_client.add_list_entry(entry, sheet_id, tab_id)

	# print ""
	# print entry
	# print ""

    # close the file connection
	log_file.close()
	# empty the log file
	open('error_log.txt', 'w').close()



