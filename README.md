
# raspberrypi-speedtest

Inspired by Make magazine http://makezine.com/projects/send-ticket-isp-when-your-internet-drops/ 


# Setup

## Prep your Raspberry Pi for doing the speedtest, per the article 

* `sudo apt-get install python-pip`
* `sudo pip install speedtest-cli`


### Test

* `speedtest-cli` 
* `speedtest-cli --simple` 


### Install the extras

* `sudo apt-get update`
* `sudo apt-get install git`
* `git clone https://github.com/HenrikBengtsson/speedtest-cli-extras.git` 


### Test

* `/home/pi/speedtest-cli-extras/bin/speedtest-csv` 


## Prep your Raspberry Pi for saving the speedtest results (via this project)

### Install google api client for python

* `git clone https://github.com/google/gdata-python-client.git`
* `cd gdata-python-client; sudo python ./setup.py install`


### Clone this project

* `git clone https://github.com/scottvlaminck/raspberrypi-speedtest`
* `cd raspberrypi-speedtest`


### Config this project

* Create a google spreadsheet via https://docs.google.com/spreadsheets/u/0/ 
	* With the following headers in the first row:

> `ConnectionType	startdate	stopdate	provider	ip	speedtestserver	distance	pingtime	downloadspeed	uploadspeed	resultimg`

* Get the id (which you can get from the url, e.g.: https://docs.google.com/spreadsheets/d/**SPREADSHEET-ID**/edit#gid=0)
* Create a gdocs app with oauth creds via https://console.developers.google.com/project and for that app: 
	* Create an OAuth 2.0 client ID
	* Enable Google Drive API
* Rename gsheet.cfg to gsheet_add.cfg
	* `mv gsheet.cfg gsheet_add.cfg`
* Update `gsheet_add.cfg` with sheet id and oauth client + secret
* Get an oauth token
	* `python get_auth_token.py`
	* Update `gsheet_add.cfg` with oauth & refresh tokens 


### Test this thing

* `run.sh` 
	* NOTE: This `run.sh` script is helpful, but very naive. It assumes that this project lives side-by-side with the speedtest-cli-extras/ directory. If that's not true, you should skip using it.
* verify the sheet has a row of data 


## Run the script at the top of each hour

### Add it to cron

* `crontab -e`
* In the resulting editor, add the following line: 

> `0 * * * * /home/pi/raspberrypi-speedtest/run.sh`


### Graph the data

* Update the spreadsheet to graph the data 







