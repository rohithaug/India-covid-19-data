import sqlite3

conn = sqlite3.connect('covid_cases.sqlite')
cur = conn.cursor()

print("---INDIA COVID-19 DATA---")

cur.execute('''
            SELECT SUM(Cases.confirmed), SUM(Cases.active), 
            SUM(Cases.recovered), SUM(Cases.deceased) 
            FROM Cases
            ''')
data = cur.fetchone()    

print("Confirmed:", data[0])
print("Active:", data[1])
print("Recovered:", data[2])
print("Deceased:", data[3])

choice = int(input('Enter 1 to view data by state and 0 to quit: '))

if choice == 1:
    print("\nList of states:")
    cur.execute('''
                SELECT States.state, SUM(Cases.confirmed), SUM(Cases.active), 
                SUM(Cases.recovered), SUM(Cases.deceased) 
                FROM Cases JOIN States
                ON Cases.state_id = States.id
                GROUP BY States.state
                ORDER BY States.state
                ''')
    
    state_index = 0
    states = []
    states_confirmed = []
    states_active = []
    states_recovered = []
    states_deceased = []
    for row in cur:
        state_index += 1
        states.append(row[0])
        states_confirmed.append(row[1])
        states_active.append(row[2])
        states_recovered.append(row[3])
        states_deceased.append(row[4])
        print(state_index,":",row[0])
    
    in_state = int(input("Enter state index to view data: "))
    print("\nState selected :",states[in_state - 1])
    print("Confirmed:", states_confirmed[in_state - 1])
    print("Active:", states_active[in_state - 1])
    print("Recovered:", states_recovered[in_state - 1])
    print("Deceased:", states_deceased[in_state - 1])
    choice = int(input('Enter 1 to view data by district and 0 to quit: '))
    
    if choice == 1:
        cur.execute('''
                    SELECT Districts.district 
                    FROM Cases JOIN States JOIN Districts JOIN Zones 
                    ON Cases.state_id = States.id 
                    AND Cases.district_id = Districts.id 
                    AND Cases.zone_id = Zones.id
                    WHERE States.state = ?
                    ORDER BY Districts.district
                    ''', (states[in_state - 1], ))
        
        print("\nDistricts in",states[in_state - 1]+":")
        district_index = 0
        districts = []
        for row in cur:
            district_index += 1
            districts.append(row[0])
            print(district_index,":",row[0])
        
        in_district = int(input("Enter district index to view data: "))
        #print("District selected :", districts[in_district - 1])
        
        cur.execute('''
                    SELECT Zones.zone, Cases.confirmed, Cases.active, Cases.recovered, Cases.deceased
                    FROM Cases JOIN States JOIN Districts JOIN Zones 
                    ON Cases.state_id = States.id 
                    AND Cases.district_id = Districts.id 
                    AND Cases.zone_id = Zones.id
                    WHERE States.state = ? AND Districts.district = ?
                    ORDER BY Cases.confirmed, Cases.active, Cases.recovered, Cases.deceased
                    ''', (states[in_state - 1], districts[in_district - 1]))
        
        for row in cur:
            zone = row[0]
            confirmed = row[1]
            active = row[2]
            recovered = row[3]
            deceased = row[4]
            
        print('\nDistrict selected:',districts[in_district - 1])
        print('Zone:',zone)
        print('Confirmed Cases:',confirmed)
        print('Active Cases:',active)
        print('Recovered:',recovered)
        print('Deceased:',deceased)
       
conn.commit()        
cur.close()
