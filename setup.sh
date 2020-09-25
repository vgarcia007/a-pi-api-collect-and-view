#!/bin/bash

#get current directory
current_working_dir=$(pwd)
#install python and venv
apt-get install python3 python3-venv
#create and activate environment
python3 -m venv apps
cd apps
source ./bin/activate
#installe required python packages
pip3 install -r requirements.txt
cd ..
#stop service in case its allready installed
systemctl stop a_pi_api_frontend
#create .service file
sed "s|__APP_DIR__|$current_working_dir|g" <a_pi_api_frontend.template.service >a_pi_api_frontend.service
mv a_pi_api_frontend.service /etc/systemd/system/a_pi_api_frontend.service
#lets go
systemctl daemon-reload
systemctl start a_pi_api_frontend
systemctl enable a_pi_api_frontend
systemctl status a_pi_api_frontend

#stop service in case its allready installed
systemctl stop a_pi_api_collector
#create .service file
sed "s|__APP_DIR__|$current_working_dir|g" <a_pi_api_collector.template.service >a_pi_api_collector.service
mv a_pi_api_collector.service /etc/systemd/system/a_pi_api_collector.service
#lets go
systemctl daemon-reload
systemctl start a_pi_api_collector
systemctl enable a_pi_api_collector
systemctl status a_pi_api_collector

echo "you can reach the frontend at http://$(hostname):8888"
