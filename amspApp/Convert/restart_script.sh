#!/bin/bash

trap "exit" INT TERM

while true; do
  echo "start.........."
  echo "start.........."
  echo "start.........."
  echo "start.........."
  echo "start.........."
  /home/mohammad/AmsPlusEnvPy36/bin/python /var/www/amsPlus/manage.py shell < /var/www/amsPlus/amspApp/Convert/start.py
  sleep 50  # 300 seconds = 5 minutes
  echo "stop.........."
  echo "stop.........."
  echo "stop.........."
  echo "stop.........."
  echo "stop.........."
  echo "stop.........."
  pkill -f manage.py
done
