import sqlite3
import csv

conn = sqlite3.connect('covid_cases.sqlite')
#conn = sqlite3.connect('covid_cases_offline.sqlite')
cur = conn.cursor()

fields = ['State', 'District', 'Zone', 'Confirmed', 'Active', 'Recovered', 'Deceased']
fname = 'covid_data.csv'

fh = open(fname, 'w')
csvwriter = csv.writer(fh)
csvwriter.writerow(fields) 

cur.execute('''
                SELECT States.state, Districts.district, Zones.zone,
                Cases.confirmed, Cases.active, Cases.recovered, Cases.deceased 
                FROM Cases JOIN States JOIN Districts JOIN Zones
                ON Cases.state_id = States.id
                AND Cases.district_id = Districts.id
                AND Cases.zone_id = Zones.id
                ORDER BY States.state, Districts.district
                ''')

for row in cur:
    state = row[0]
    districts = row[1]
    zones = row[2]
    confirmed = row[3]
    active = row[4]
    recovered = row[5]
    deceased = row[6]
    csvwriter.writerow([state,districts,zones,confirmed,active,recovered,deceased])

print("Data extracted and written to covid_data.csv file.\nOpen visualize.twb to visualize the data.")