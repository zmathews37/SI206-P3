#Call API to get team roster and add each player into database table called Players
#For each of these players, call API to get player stats and add to database table called Statistics

import requests
import sqlite3

urlbaseMLB = "http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2017'"

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
    cursor.execute('DROP TABLE Teams')
    connection.commit()
    connection.close()

def get_connection():
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    return connection, cursor

def put_player_in_database(name, team, position, player_id):
    ret = get_connection()
    connection = ret[0]
    cursor = ret[1]

    cursor.execute('CREATE TABLE IF NOT EXISTS Players (name TEXT, team TEXT, position TEXT, player_id)')
    cursor.execute('INSERT INTO Players VALUES ("' + name + '", "' + team + '", "' + position + '", "' + player_id + '")')

    connection.commit()
    connection.close()
    return None

def put_full_roster_in_database(team_name, year):
    resp = get_roster(team_name, year)
    for player in resp:
        name = player["name_first_last"]
        team = player["team_code"]
        position = player["position_txt"]
        player_id = player["player_id"]
        put_player_in_database(name, team, position, player_id)
    return None

def main():
    put_full_roster_in_database("Houston Astros", "2017")

    #db.connection_test()


    #algorithm:
    #1. get team roster from MLB API and add to database
    #2. for each player, get player info from MLB API and add to database

if __name__ == "__main__":
    main()
