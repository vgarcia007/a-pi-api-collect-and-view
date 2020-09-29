#!/bin/bash
if [ -z "$1" ] 
   then
     setup_type="production"
 else
     setup_type="dev"
 fi

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

if [ setup_type  = "dev" ]; then
    cd apps
    export FLASK_ENV=development
    python3 flask-frontend.py
else
    #stop collector service in case its allready installed
    systemctl stop a_pi_api_collector

    #create collector .service file
    sed "s|__APP_DIR__|$current_working_dir|g" <a_pi_api_collector.template.service >a_pi_api_collector.service
    mv a_pi_api_collector.service /etc/systemd/system/a_pi_api_collector.service

    #reload and enable
    systemctl daemon-reload
    systemctl enable a_pi_api_collector
    systemctl start a_pi_api_collector

    #stop frontend service in case its allready installed
    systemctl stop a_pi_api_frontend

    #create frontend .service file
    sed "s|__APP_DIR__|$current_working_dir|g" <a_pi_api_frontend.template.service >a_pi_api_frontend.service
    mv a_pi_api_frontend.service /etc/systemd/system/a_pi_api_frontend.service

    #reload and enable
    systemctl daemon-reload
    systemctl enable a_pi_api_frontend
    systemctl start a_pi_api_frontend

    #finished
    echo "you can reach the frontend at http://$(hostname):8888"
fi


