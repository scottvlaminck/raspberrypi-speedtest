#!/bin/sh

PATH=$PATH:/usr/local/bin

cd `dirname $0`
../speedtest-cli-extras/bin/speedtest-csv | python gsheet_add.py
