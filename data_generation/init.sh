#!/bin/bash

apt-get update
#apt-get install python3 -y
#apt-get install python3-pip -y
pip install --upgrade pip --break-system-packages
pip install -r /dependencies/requirements.txt --break-system-packages