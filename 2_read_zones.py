import urllib.request, urllib.parse, urllib.error
import sqlite3
import json

conn = sqlite3.connect('covid_cases.sqlite')
cur = conn.cursor()

cur.executescript ('''
DROP TABLE IF EXISTS Zones;
                
CREATE TABLE IF NOT EXISTS "Zones" (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "zone" TEXT UNIQUE
            )
''')

'''
#use data downloaded file from https://api.covid19india.org/ and saved as district_wise.json     
fname = 'zones.json'
fh = open(fname)
data = fh.read()
'''

#from online
url = 'https://api.covid19india.org/zones.json'
print('Retrieving', url) 
info = urllib.request.urlopen(url)
data = info.read().decode()

#read data
js = json.loads(data)
#print(js)

for value in js["zones"]:
    state = value["state"]
    cur.execute('INSERT OR IGNORE INTO States(state) VALUES(?)', (state, ))
    cur.execute('SELECT id FROM States WHERE state = ?', (state, ))
    state_id = cur.fetchone()[0]
    
    district = value["district"]
    cur.execute('INSERT OR IGNORE INTO Districts(district) VALUES(?)', (district, ))
    cur.execute('SELECT id FROM Districts WHERE district = ?', (district, ))
    district_id = cur.fetchone()[0]

    cur.execute('SELECT id FROM Cases WHERE state_id = ? AND district_id = ?', (state_id, district_id))
    x = cur.fetchone()
    
    if x is None:
        cur.execute('''INSERT OR IGNORE INTO Cases(state_id, district_id, confirmed, active, recovered, deceased)
                    VALUES(?, ?, 0, 0, 0, 0)''', (state_id, district_id))

conn.commit()

for value in js["zones"]:
    #print("State:", value["state"])
    state = value["state"]
    cur.execute('SELECT id FROM States WHERE state = ?', (state, ))
    state_id = cur.fetchone()[0]
    
    #print("District:", value["district"])
    district = value["district"]
    cur.execute('SELECT id FROM Districts WHERE district = ?', (district, ))
    district_id = cur.fetchone()[0]

    #print("Zone:", value["zone"])
    zone = value["zone"]
    cur.execute('INSERT OR IGNORE INTO Zones(zone) VALUES(?)', (zone, ))
    cur.execute('SELECT id FROM Zones WHERE zone = ?', (zone, ))
    zone_id = cur.fetchone()[0]
    
    cur.execute('SELECT id FROM Cases WHERE state_id = ? AND district_id = ?', (state_id, district_id))
    case_id = cur.fetchone()[0]
    
    cur.execute('UPDATE Cases SET zone_id=? WHERE id=?', (zone_id, case_id))

conn.commit()
#Update NULL Values
cur.execute('SELECT id FROM Zones WHERE zone = ?',('',))
zone_id = cur.fetchone()[0]
cur.execute('UPDATE Cases SET zone_id = ? WHERE zone_id is NULL', (zone_id,))

print("Updated Zone data.")   
conn.commit()        
cur.close()