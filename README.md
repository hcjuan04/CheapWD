# CheapWD
Wardriving in python


WARNING - - This is and on going project - please feedback to me

1. Make suer your create your DB structure - cheapWD-DB.sql

2. Install requirements.txt 
   #pip install requirements.txt

3. Stop proccesses and and put your interfaces in monitor mode
   #./interfaces.sh
   
 4. Fill in cheaparam.py
 
 5. Read the comments on kml_plot - lines 199 to 202
 
 6.Run cheapWD_v3.3.py
 
 GPS with your mobile phone
 
 1. If it's android, you'll activate developer mode and turn on debug.
 2. Install sharegps on your android (you can follow this to set it up, just the part of the GPS https://holisticsecurity.io/2016/02/27/wardriving-wifi-pineapple-nano-mobile-world-congress-2016-barcelona/)
 3. Install gpsd and adb
 4. Set up the gps
    #adb devices -- make sure your device in attached
    #adb forward tcp:50000 tcp:50000 
    #gpsd -N tcp://127.0.0.1:50000
