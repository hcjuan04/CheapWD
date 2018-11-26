#!/bin/bash
echo "killing wifi process"
airmon-ng check kill
ifconfig wlan0 down
ifconfig wlan1 down
ifconfig wlan2 down
ifconfig wlan3 down
echo "wlan0-3  down"
iwconfig wlan0 mode monitor
iwconfig wlan1 mode monitor
iwconfig wlan2 mode monitor
iwconfig wlan3 mode monitor
echo "wlan0-3 monitor mode "
ifconfig wlan0 up
ifconfig wlan1 up
ifconfig wlan2 up
ifconfig wlan3 up
echo "wlan0-3 up "
