# Name: start.sh
# Author: Reacubeth
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

#! /usr/bin/env bash

set -ex

PORT=${PORT0:-7861}
#exec python app.py $PORT 
exec python -m uvicorn app:app --host 127.0.0.1 --port $PORT
