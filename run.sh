#!/bin/bash

set -o pipefail

PATH=$PATH:/usr/local/bin

cd `dirname $0`

curl "http://www.google.co.uk" --max-time 5
result=$?

if [ $result -ne 0 ]; then
  echo "error" | python gsheet_add.py
else
  ../speedtest-cli-extras/bin/speedtest-csv | python gsheet_add.py
fi