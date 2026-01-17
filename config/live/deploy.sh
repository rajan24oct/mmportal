#!/usr/bin/env bash

cd /opt/apps/mmportal/
git pull origin main
source /home/admin/.virtualenvs/hr_automation/bin/activate
pip install -r /opt/apps/mmportal/requirements.txt
/home/admin/.virtualenvs/hr_automation/bin/python manage.py migrate
/home/admin/.virtualenvs/hr_automation/bin/python manage.py collectstatic --noinput
sudo supervisorctl stop mmportal
sudo kill -9 $(lsof -t -i:8000)
sudo supervisorctl start mmportal
