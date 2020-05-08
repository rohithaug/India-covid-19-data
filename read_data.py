import urllib.request, urllib.error
import sqlite3
import json

conn = sqlite3.connect('covid_cases.sqlite')
cur = conn.cursor()

cur.executescript ('''
DROP TABLE IF EXISTS States;
DROP TABLE IF EXISTS Districts;
DROP TABLE IF EXISTS Cases;
                
CREATE TABLE IF NOT EXISTS "States" (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "state" TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS "Districts" (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "district" TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS "Cases"
            ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
            "state_id" INTEGER, 
            "district_id" INTEGER,
            "zone_id" INTEGER,
            "confirmed" INTEGER, 
            "active" INTEGER, 
            "recovered" INTEGER, 
            "deceased" INTEGER)
''')

'''
#use data downloaded file from https://api.covid19india.org/ and saved as district_wise.json     
fname = 'district_wise.json'
fh = open(fname)
data = fh.read()
'''
#from online
url = 'https://api.covid19india.org/state_district_wise.json'
print('Retrieving', url) 
info = urllib.request.urlopen(url)
data = info.read().decode()

#read data
js = json.loads(data)
#print(js)

#country
#country_count_confirmed = 0
#country_count_active = 0
#country_count_recovered = 0
#country_count_deceased = 0
    
#states
for state in js:
    #print(state)
    state_count_confirmed = 0
    state_count_active = 0
    state_count_recovered = 0
    state_count_deceased = 0
    
    cur.execute('INSERT OR IGNORE INTO States(state) VALUES(?)', (state, ))
    cur.execute('SELECT id FROM States WHERE state = ?', (state, ))
    state_id = cur.fetchone()[0]

    #districts
    for district in js[state]["districtData"]:
        #print(district+":")

        cur.execute('INSERT OR IGNORE INTO Districts(district) VALUES(?)', (district, ))
        cur.execute('SELECT id FROM Districts WHERE district = ?', (district, ))
        district_id = cur.fetchone()[0]

        #confirmed
        confirmed = js[state]["districtData"][district]["confirmed"]
        #print("Confirmed:", confirmed)
        state_count_confirmed += int(confirmed)

        #recovered
        recovered = js[state]["districtData"][district]["recovered"]
        #print("Recovered:", recovered)
        state_count_recovered += int(recovered)      

        #deceased
        deceased = js[state]["districtData"][district]["deceased"]
        #print("Deceased:", deceased)
        state_count_deceased += int(deceased)
        
        #active
        active = confirmed - (recovered + deceased)
        #print("Active:", active)
        state_count_active += active
        
        cur.execute('''INSERT OR IGNORE INTO Cases(state_id, district_id, confirmed, active, recovered, deceased) 
                    VALUES(?, ?, ?, ?, ?, ?)''', (state_id, district_id, confirmed, active, recovered, deceased))
         
    #print("Total confirmed :",state_count_confirmed)
    #print("Total active :",state_count_active)
    #print("Total recovered :",state_count_recovered)
    #print("Total deceased :",state_count_deceased)
    #print("\n")
    #country_count_confirmed += state_count_confirmed
    #country_count_active += state_count_active
    #country_count_recovered += state_count_recovered
    #country_count_deceased += state_count_deceased

#print(country_count_confirmed,country_count_active, country_count_recovered, country_count_deceased)

print("Data Retrieved.")        
conn.commit()        
cur.close()
