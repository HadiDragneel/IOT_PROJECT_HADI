#!/bin/bash

API="o.j9pYLoz9MkkdvQ71U3NORDYpNJXy6exd"
MSG="$1"

curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Intruder Alert" -d body="$MSG"
