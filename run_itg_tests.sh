#!/bin/bash

./run.sh &
sleep 5
FLASK_PID=$!
nose2 -v -c ./itgtest.cfg
echo "PID:  $FLASK_PID"
kill $FLASK_PID
lsof -i :5000 -sTCP:LISTEN |awk 'NR > 1 {print $2}'|xargs kill -15


