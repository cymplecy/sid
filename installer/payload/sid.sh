#!/bin/bash
#Version 0.2 - add in & to allow simulatenous running of handler and Scratch
#Version 0.3 - change sp launches rsc.sb from "/home/pi/Documents/Scratch Projects"
#Version 0.4 - 20Mar13 meltwater - change to use provided name for home
#V0.5 re-used for launching sid.py
#V5.0 for sgh5
sudo pkill -f sid.py 
sudo python /home/pi/sid/sid.py
