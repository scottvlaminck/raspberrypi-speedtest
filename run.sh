#!/bin/sh

../speedtest-cli-extras/bin/speedtest-csv | python gsheet_add.py
