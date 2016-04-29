#!/bin/sh

cd `dirname $0`
../speedtest-cli-extras/bin/speedtest-csv | python gsheet_add.py
