#! /usr/bin/python
# License: GPL 2.0

import sys, os, signal
import datetime
from scapy.all import *
from multiprocessing import Process
import threading
import datetime
from gps import *
import psycopg2
from cheaparam import sniffint, probeint, clientint, user_db, database, passw, hostdb
import time

interface = sniffint
interface2 = probeint
interface3 = clientint
snifAPp = None
ppid = 0
ppid2 = 0
ppid3 = 0
ppid4 = 0
ppid5 = 0
dbuser = user_db
dtabase = database
password = passw
dbhost = hostdb
gpsd = None #seting the global variable
conn = psycopg2.connect(host=dbhost,database=dtabase, user=dbuser, password=password)
conn2 = psycopg2.connect(host=dbhost,database=dtabase, user=dbuser, password=password)
conn3 = psycopg2.connect(host=dbhost,database=dtabase, user=dbuser, password=password)

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        global ppid4
        ppid4= os.getpid()
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

class CSniffAP(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_value = None
        self.running = True #setting the thread running to true
        signal.signal(signal.SIGINT, self.signal_handler1)
        global gpsd
        global ppid
        ppid = os.getpid()
    def sniffAP(self,p):
        try:
            global conn
            if p.haslayer(Dot11Beacon):
                try:
                    extra = p.notdecoded
                    rssi = -(256-ord(extra[-4:-3]))
                except:
                    rssi = -100
                ssid = str(p[Dot11Elt].info)
                #print ssid.encode('hex')
                #print p[Dot11].addr3
                if ssid.encode("hex")== "" : ssid = "-"
                if (int(ssid.encode("hex"), 16) == 0): ssid = "-"
                bssid2 = p[Dot11].addr3
                #bssid2 = p.addri3
                channel = int( ord(p[Dot11Elt:3].info))
                capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}{Dot11ProbeResp:%Dot11ProbeResp.cap%}")
                if re.search("privacy", capability): enc = 'Y'
                else: enc  = 'N'
                tstamp=str(datetime.datetime.today())
                if str(gpsd.fix.latitude) == "nan":
                    lat = 0.0
                else : lat= gpsd.fix.latitude
                if str(gpsd.fix.longitude) == "nan":
                    longt= 0.0
                else : longt= gpsd.fix.longitude
                if str(gpsd.fix.altitude) == "nan":
                    alt = 0.0
                else : alt = gpsd.fix.altitude
                #lat = 6.0000
                #longt = -75.111188833
                #alt = 1597.4
                print "Beacon|" +tstamp +"|"+str(rssi) +"|"+str(channel) + "|" + enc + "|" + bssid2 + "|" + ssid + "|" + str(lat) + "|" + str(longt) + "|" + str(alt)
                query = "INSERT INTO beacon (tstamp, channel, rssi, enc, bssid, ssid, lat, long, alt) VALUES (" +"'"+tstamp+"'"+","+str(channel)+","+str(rssi)+","+"'"+enc+"'"+","+"'"+ bssid2 +"'"+","+"'"+ssid+"'"+","+str(lat)+","+str(longt)+","+str(alt)+")"
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
			print "interrupted"

    def run(self):
		global interface
		sniff(iface=interface,prn=self.sniffAP, store=0)

    def signal_handler1 (self, signal, frame):
        print "signal handler 1"

class CSniffProbe (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_value = None
        self.running = True #setting the thread running to true
        signal.signal(signal.SIGINT, self.signal_handler2)
        global ppid3
        ppid3 = os.getpid()
    def sniffProbe(self,p):
        global conn2
        try:
            if p.haslayer(Dot11):
                if p.type == 0 and p.subtype == 4 :
                    timestamp = datetime.datetime.today()
                    tstamp = str(timestamp)
                    if str(gpsd.fix.latitude) == "nan":
                        lat = 0.0
                    else : lat= gpsd.fix.latitude
                    if str(gpsd.fix.longitude) == "nan":
                        longt= 0.0
                    else : longt= gpsd.fix.longitude
                    if str(gpsd.fix.altitude) == "nan":
                        alt = 0.0
                    else : alt = gpsd.fix.altitude
                    #lat = 6.0000
                    #longt = -75.111188833
                    #alt = 1597.4
                    sta = p.addr2
                    ssid = p.info
                    CBLUE   = '\33[34m'
                    CEND      = '\33[0m'
                    print CBLUE +"Probe|" +tstamp+"|"+ p.addr2 + "|" + p.info + "|" + str(lat) + "|" + str(longt) + "|" + str(alt)+CEND
                    query2 = "INSERT INTO probe (tstamp, probeaddr, ssid, lat, long, alt) VALUES (" +"'"+tstamp+"'"+","+"'"+sta+"'"+","+"'"+ssid+"'"+","+str(lat)+","+str(longt)+","+str(alt)+")"
                    cur2 = conn2.cursor()
                    cur2.execute(query2)
                    conn2.commit()
        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print "interrupted"
    def run(self):
        global interface2
        print interface2
        sniff(iface=interface2,prn=self.sniffProbe, store=0)
    def signal_handler2(self, signal, frame):
        print "signal handler 2+"


class CSniffClient (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_value = None
        self.running = True #setting the thread running to true
        signal.signal(signal.SIGINT, self.signal_handler3)
        global ppid5
        ppid5 = os.getpid()
    def sniffClient (self,p):
        global conn3
        try:
            if p.haslayer(Dot11) and p.type == 2:
                timestamp = datetime.datetime.today()
                tstamp = str(timestamp)
                stacli= p.addr2
                bssid3= p.addr3
                CBLUE   = '\33[91m'
                CEND      = '\33[0m'
                print CBLUE +"client|" +tstamp+"|"+ p.addr2 + "|" + p.addr3 +CEND
                query2 = "INSERT INTO client (tstamp, sta, bssid) VALUES (" +"'"+tstamp+"'"+","+"'"+stacli+"'"+","+"'"+bssid3+"'"+")"
                cur3 = conn3.cursor()
                cur3.execute(query2)
                conn3.commit()
        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
            print "interrupted"
    def run(self):
        global interface3
        sniff(iface=interface3,prn=self.sniffClient, store=0)
        print interface3
        print "------------cleint---------"
    def signal_handler3(self, signal, frame):
        print "signal handler 3"

def channel_hopper():
    global ppid2
    ppid2 = os.getpid()
    while True:
        try:
            channel = random.randrange(1,11)
            os.system("iw dev %s set channel %d" % (interface, channel))
            os.system("iw dev %s set channel %d" % (interface2, channel))
            os.system("iw dev %s set channel %d" % (interface3, channel))
        except KeyboardInterrupt:
            break

def signal_handler (signal, frame) :
    p.terminate()
    p.join()
    sys.exit(0)

if __name__ == '__main__':
    gpsp = GpsPoller() # create the thread
    snifclient = CSniffClient()
    snifAPp = CSniffAP ()
    snifProbep = CSniffProbe ()
    try:
        gpsp.start() # start it up gps
        p = Process(target = channel_hopper)
        p.start()
        signal.signal(signal.SIGINT, signal_handler)
        print "start"
        snifclient.start()
        snifProbep.start()
        snifAPp.start()
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "Done.\nExiting."
        print "+++++++"
        print ppid
        print ppid2
        print ppid3
        print ppid4
        print "+++++++"
        os.system ("kill %d" % (ppid))
        os.system ("kill %d" % (ppid2))
        os.system ("kill %d" % (ppid3))
        os.system ("kill %d" % (ppid4))
        os.system ("kill %d" % (ppid5))
