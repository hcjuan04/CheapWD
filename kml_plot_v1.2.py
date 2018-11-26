#! /usr/bin/python
# License: GPL 2.0
import psycopg2
import simplekml
import pdb
from cheaparam import user_db, database, passw, hostdb
dbuser = user_db
dtabase = database
dbhost = hostdb
password = passw
conn = None
cur = None

class iniplot :
    def __init__(self):
        global dbuser
        global dtabase
        global password
        global dbhost
        global conn
        global cur
        try:
            conn = psycopg2.connect(host=dbhost,database=dtabase, user=dbuser, password=password)
            cur = conn.cursor()
            cur.execute("drop table if exists beacon_u")
            conn.commit()
            cur.execute("create table beacon_u as select distinct channel, bssid, ssid, rssi, lat, long from beacon where lat != 0 and long != 0 order by ssid")
            conn.commit()
            cur.execute("drop table if exists probe_u")
            conn.commit()
            cur.execute("create table probe_u as select distinct probeaddr, ssid, lat, long from probe where lat != 0 and long != 0")
            conn.commit()
            cur.execute("drop table if exists beacon_med")
            conn.commit()
            cur.execute("create table beacon_med as select max(lat) as max_lat, max(long) as max_long, min(lat) as min_lat, min(long) as min_long, (( max(lat) +  min(lat))/2) as med_lat, (( max(long) +  min(long))/2) as med_long, bssid, ssid from beacon_u group by bssid, ssid")
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def kml_fill(self, kmlname) :
        global conn
        global cur
        kml = simplekml.Kml()
        cur = conn.cursor()
        cur.execute("select count(*) from beacon_u")
        row =cur.fetchone()
        print row[0]
        print row
        print kmlname
        i=0
        bquery = "select * from beacon_u limit 1 offset "
        while i < row[0]:
            cur.close()
            cur = conn.cursor()
            query = bquery + str(i)
            cur.execute(query)
            row2 =cur.fetchone()
            print row2
            channel= row2[0]
            bssid= row2[1].strip()
            ssid= row2[2].strip()
            rssi= row2[3]
            lat= row2[4]
            longt= row2[5]
            desc = str(channel)+" || "+ bssid + " || "+str(rssi)
            pnt = kml.newpoint(name=ssid, description=desc,coords=[(longt,lat)])
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/target.png'
            if rssi > -37:
                pnt.style.iconstyle.color = simplekml.Color.red  # Make red
            elif rssi >= -55 and rssi <= -37:
                pnt.style.iconstyle.color = simplekml.Color.yellow  # Make red
            else:
                pnt.style.iconstyle.color = simplekml.Color.green  # Make red

            i=i+1
        print i
        print row[0]
        print row
        print kmlname
        kml.save(kmlname)
        conn.close()

    def kml_plotone(self, kmlname, fssid) :
        global conn
        global cur
        kml = simplekml.Kml()
        cur.execute("select count(*) from beacon_u")
        row =cur.fetchone()
        print row[0]
        print row
        print kmlname
        i=0
        bquery = "select * from beacon_u limit 1 offset "
        while i < row[0]:
            cur.close()
            cur = conn.cursor()
            query = bquery + str(i)
            cur.execute(query)
            row2 =cur.fetchone()
            ssid= row2[2].strip()
            if ssid == fssid :
                print row2
                channel= row2[0]
                bssid= row2[1].strip()
                lat= row2[4]
                rssi= row2[3]
                longt= row2[5]
                desc = str(channel)+" || "+ bssid + " || "+str(rssi)
                pnt = kml.newpoint(name=ssid, description=desc,coords=[(longt,lat)])
                pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
                if rssi > -37:
                    pnt.style.iconstyle.color = simplekml.Color.red  # Make red
                elif rssi >= -55 and rssi <= -37:
                    pnt.style.iconstyle.color = simplekml.Color.yellow  # Make red
                else:
                    pnt.style.iconstyle.color = simplekml.Color.green  # Make red

            i=i+1
        print i
        print row[0]
        print row
        print kmlname
        kml.save(kmlname)
        conn.close()

    def kml_plotprobe(self, kmlname) :
        global conn
        global cur
        kml = simplekml.Kml()
        cur.close()
        cur = conn.cursor()
        cur.execute("select count(*) from probe_u")
        row =cur.fetchone()
        print row[0]
        print row
        print kmlname
        i=0
        bquery = "select * from probe_u limit 1 offset "
        while i < row[0]:
            cur.close()
            cur = conn.cursor()
            query = bquery + str(i)
            cur.execute(query)
            row2 =cur.fetchone()
            print row2
            probeaddr= row2[0].strip()
            ssid= row2[1].strip()
            lat= row2[2]
            longt= row2[3]
            desc = probeaddr + " || "+ssid
            pnt = kml.newpoint(name=probeaddr, description=desc,coords=[(longt,lat)])
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
            i=i+1
        print i
        print row[0]
        print row
        print kmlname
        kml.save(kmlname)
        conn.close()

    def kml_plotbeaconmed(self, kmlname) :
        global conn
        global cur
        kml = simplekml.Kml()
        cur.execute("select count(*) from beacon_med")
        row =cur.fetchone()
        print row[0]
        print row
        print kmlname
        i=0
        bquery = "select * from beacon_med limit 1 offset "
        while i < row[0]:
            cur.close()
            cur = conn.cursor()
            query = bquery + str(i)
            cur.execute(query)
            row2 =cur.fetchone()
            print row2
            bssid= row2[6].strip()
            ssid= row2[7].strip()
            lat= row2[4]
            longt= row2[5]
            desc = bssid + " || "+ssid
            pnt = kml.newpoint(name=probeaddr, description=desc,coords=[(longt,lat)])
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
            pnt.style.iconstyle.color = simplekml.Color.yellow
            i=i+1
        print i
        print row[0]
        print row
        print kmlname
        kml.save(kmlname)
        conn.close()

if __name__ == '__main__':
    try:
        plot = iniplot()
        plot.kml_fill("filek.kml") #not recomended plot all the data
        plot.kml_plotone("plotone.kml","MySSID") #plot just on SSID MySSID
        plot.kml_plotprobe("plotprobe.kml") # Plot probes
        plot.kml_plotbeaconmed("beaconmed.kml") # Plot med becons

    except (KeyboardInterrupt, SystemExit):
        print "Error 1"
