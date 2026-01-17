#!/usr/bin/env bash

cd /opt/apps/mmportal/
git pull origin main
source /opt/apps/mmportal/.venv/bin/activate
pip install -r /opt/apps/mmportal/requirements.txt
/opt/apps/mmportal/.venv/bin/python manage.py migrate
/opt/apps/mmportal/.venv/bin/python manage.py collectstatic --noinput
sudo supervisorctl stop mmportal
sudo kill -9 $(lsof -t -i:8000)
sudo supervisorctl start mmportal
