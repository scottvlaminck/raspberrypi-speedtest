
# see: http://stackoverflow.com/questions/15075919/gdata-python-google-apps-authentication

import ConfigParser
import gdata.gauth

config = ConfigParser.ConfigParser()
config.read('gsheet_add.cfg')

if not (config.has_option('oauth', 'client_id') and config.has_option('oauth', 'client_secret')):
    raise ValueError('auth client_id and client_secret are required')



Client_id=config.get('oauth', 'client_id')
Client_secret=config.get('oauth', 'client_secret')
Scope='https://spreadsheets.google.com/feeds/'
User_agent='rpi-speedtest-auth'

token = gdata.gauth.OAuth2Token(client_id=Client_id,client_secret=Client_secret,scope=Scope,user_agent=User_agent)

print ''
print 'open ' + token.generate_authorize_url(redirect_uri='urn:ietf:wg:oauth:2.0:oob')
print ''

code = raw_input('What is the verification code? ').strip()
token.get_access_token(code)

print ""
print "Access Token"
print token.access_token
print ""
print "Refresh token"
print token.refresh_token

print ""


# config.set('oauth_token', 'access_token', token.access_token)
# config.set('oauth_token', 'refresh_token', token.refresh_token)
# 
# with open('gsheet.cfg', 'wb') as configfile:
# 	config.write(configfile)


