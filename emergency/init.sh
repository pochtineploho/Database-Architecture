#!/bin/bash

apt-get update
pip install --upgrade pip --break-system-packages
pip install -r /dependencies/requirements.txt --break-system-packages