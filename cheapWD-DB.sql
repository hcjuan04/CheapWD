
create table beacon (tstamp TIMESTAMP, channel INT, Enc CHAR (2), bssid CHAR (20), ssid CHAR (50), lat FLOAT, long FLOAT, alt FLOAT);
create table probe (tstamp TIMESTAMP,  probeAddr CHAR (20), ssid CHAR (50), lat FLOAT, long FLOAT, alt FLOAT);
create table client (tstamp TIMESTAMP,  sta CHAR (20), bssid CHAR (20) );
