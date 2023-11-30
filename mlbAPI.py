#Call API to get team roster and add each player into database table called Players
#For each of these players, call API to get player stats and add to database table called Statistics

import requests
import sqlite3

urlbaseMLB = "http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2017'"
list_of_teams_and_years = [("Chicago Cubs", "2016"), ("Cleveland Indians", "2016"), ("Houston Astros", "2017"), ("Los Angeles Dodgers", "2017")]

def get_api_full_info(url, input_headers, input_params):
    response = requests.get(url, headers=input_headers, params=input_params)
    return response.json()

def print_team_info(filename, team_info):
    f = open(filename, "w")
    teams = team_info["team_all_season"]["queryResults"]["row"]
    for team in teams:
        f.write(str(team))
        f.write("\n")
    f.close()
    return None

def handle_team_info():
    response_team_info = get_api_full_info(urlbaseMLB, None, None)
    print_team_info("teams.txt", response_team_info)
    return None

#get team info for 2017 season astros
def get_roster(team_name, year):
    team_info = get_api_full_info(urlbaseMLB, None, None)
    teams = team_info["team_all_season"]["queryResults"]["row"]

    for team in teams:
        if team["name_display_full"] == team_name:
            team_id = team["team_id"]

    url_team_info = "http://lookup-service-prod.mlb.com/json/named.roster_team_alltime.bam?start_season='2017'&end_season='2017'&team_id='117'"
    url_team_info = url_team_info.replace("'2017'", "'" + year + "'")
    url_team_info = url_team_info.replace("'117'", "'" + team_id + "'")
    
    response = requests.get(url_team_info)
    data = response.json()
    return data["roster_team_alltime"]["queryResults"]["row"]


### DATABASE FUNCTIONS ###

#only use when needed!!!
def drop_tables(): 
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE Players')
    connection.commit()
    connection.close()

def get_connection():
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    return connection, cursor

def put_player_in_database(player_id, name, team_id, position, year):
    ret = get_connection()
    connection = ret[0]
    cursor = ret[1]

    #change this so that the key is player_id
    cursor.execute('CREATE TABLE IF NOT EXISTS Players (player_id INTEGER PRIMARY KEY, name TEXT, team_id INTEGER, position TEXT, year INTEGER)') 
    cursor.execute('INSERT INTO Players VALUES (?, ?, ?, ?, ?)', (player_id, name, team_id, position, year))

    connection.commit()
    connection.close()
    return None

def put_full_roster_in_database(team_name, year):
    resp = get_roster(team_name, year)
    for player in resp:
        player_id = player["player_id"]
        name = player["name_first_last"]
        team_id = player["team_id"]
        position = player["position_desig"]
        put_player_in_database(player_id, name, team_id, position, int(year))
    return None

def main():
    for tup in list_of_teams_and_years:
        put_full_roster_in_database(tup[0], tup[1])

    #db.connection_test()


    #algorithm:
    #1. get team roster from MLB API and add to database
    #2. for each player, get player info from MLB API and add to database

if __name__ == "__main__":
    main()
