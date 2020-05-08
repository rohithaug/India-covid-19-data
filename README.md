#INDIA-COVID-19-DATA

Extracting and visualizing the covid-19 data of India live using Python.

This is a set of code you can use to extract data and visualize from the json file provided at:
https://api.covid19india.org/ (Thanks to the respective developers).

1. read_data.py extracts the covid-19 data from the json file and saves it in a SQLite database 'covid_cases.sqlite'.

    Output:
    Retrieving https://api.covid19india.org/state_district_wise.json
    Data Retrieved.

    This shows your code was successfull extracting the covid data from the json file.

2. read_zones.py extracts the Zone of each district and updates the data to the SQLite database 'covid_cases.sqlite'.
    Both these codes models the data so that it takes minimal space i.e. no replica of data is saved in the database,
    for example, States, Districts, Zones, etc.

    Output:
    Retrieving https://api.covid19india.org/zones.json
    Updated Zone data.

    This shows your code was successfull extracting and updating the databses with the zone data of each district from the json file.

These codes collects data directly from the link, if required it can be modified to obtain data from json file stored offline.

DB Browser (SQLite) or any other SQL browser can be used to view the database 'covid_cases.sqlite'.
You can download the brower from:
http://sqlitebrowser.org/

3. Run find_data.py to look through the database and view the COVID-19 cases in the country, state-wise and ditrict-wise.
    The code will run you through the database as per your requirement.

If you just want to look the data, you can download the 'covid_cases.sqlite' and directly run the find_data.py to
look through the data. But the provided database will contain only COVID19 data until 8th May 2020 - IST 05:00 P.M. If you
want to update the recent data, run read_data.py and read_zones.py files first and then run the find_data.py file.

If you require, you can alter the find_data.py to visualize the data as per your requirement.

4. I have also provided the file extract_data.py which you can use to save the data as a .csv file. You can use that as well
    to visualize the data using Excel or any suitable tools as per your requirement.
    
Suggestions and comments are welcome!

--ROHITH S P
