#Call API to get team roster and add each player into database table called Players
#For each of these players, call API to get player stats and add to database table called Statistics

#important info:
#player_id is unique for each player for each year
#integer key is player_id+year

import requests
import sqlite3

urlbaseMLB = "http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2017'"
list_of_teams_and_years = [("San Francisco Giants", "2012"), ("Detroit Tigers", "2012"), ("Houston Astros", "2017"), ("Los Angeles Dodgers", "2017")]

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

def get_player_statistics(player_id, position, year, team_id):
    if (position != "PITCHER"):
        url_player_info = "http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2017'&player_id='493316'"
        url_player_info = url_player_info.replace("'2017'", "'" + year + "'")
        url_player_info = url_player_info.replace("'493316'", "'" + player_id + "'")
        response = requests.get(url_player_info)
        data = response.json()
        results = data["sport_hitting_tm"]["queryResults"]["row"]
        if len(results) > 1 and len(results) < 5:
            for team in results:
                if team["team_id"] == team_id:
                    return team
        return results
    else:
        url_player_info = "http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam?league_list_id='mlb'&game_type='R'&season='2017'&player_id='592789'"
        url_player_info = url_player_info.replace("'2017'", "'" + year + "'")
        url_player_info = url_player_info.replace("'592789'", "'" + player_id + "'")
        response = requests.get(url_player_info)
        data = response.json()
        results = data["sport_pitching_tm"]["queryResults"]["row"]
        if len(results) > 1 and len(results) < 5:
            for team in results:
                if team["team_id"] == team_id:
                    return team
        return results


### DATABASE FUNCTIONS ###

#only use when needed!!!
def drop_tables(): 
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS Players')
    cursor.execute('DROP TABLE IF EXISTS Statistics')
    connection.commit()
    connection.close()
    return None

def get_connection():
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    return connection, cursor

def add_player_to_Players_table(player_id, name, team_id, position, year):
    ret = get_connection()
    connection = ret[0]
    cursor = ret[1]

    #change this so that the key is player_id
    player_id = str(player_id) + str(year)
    player_id = int(player_id)
    cursor.execute('CREATE TABLE IF NOT EXISTS Players (player_id INTEGER PRIMARY KEY, name TEXT, team_id INTEGER, position TEXT, year INTEGER)') 
    cursor.execute('INSERT INTO Players VALUES (?, ?, ?, ?, ?)', (player_id, name, team_id, position, year))

    connection.commit()
    connection.close()
    return None

def add_player_to_Statistics_table(player_id, position, year, team_id):
    ret = get_connection()
    connection = ret[0]
    cursor = ret[1]

    stats = get_player_statistics(player_id, position, year, team_id)

    if (position != "PITCHER"):
        homeruns = stats["hr"]
        ops  = stats["ops"]
        hitter_strikeouts = stats["so"]
        games = stats["g"]
    else:
        era = stats["era"]
        whip = stats["whip"]
        pitcher_strikeouts = stats["so"]
        games = stats["g"]


    cursor.execute('CREATE TABLE IF NOT EXISTS Statistics (player_id INTEGER PRIMARY KEY, position TEXT, year INTEGER, team_id INTEGER, games INTEGER, homeruns INTEGER, ops REAL, hitter_strikeouts INTEGER, era REAL, whip REAL, pitcher_strikeouts INTEGER)')

    player_id = str(player_id) + str(year)
    player_id = int(player_id)
    if (position != "PITCHER"):
        cursor.execute('INSERT INTO Statistics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (player_id, position, year, team_id, games, homeruns, ops, hitter_strikeouts, None, None, None))
    else:
        cursor.execute('INSERT INTO Statistics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (player_id, position, year, team_id, games, None, None, None, era, whip, pitcher_strikeouts))

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
        add_player_to_Players_table(player_id, name, team_id, position, int(year))
        add_player_to_Statistics_table(player_id, position, year, team_id)
    return None

def main():
    #algorithm:
    #1. get team roster from MLB API and add to database
    #2. for each player, get player info from MLB API and add to database

    drop_tables()
    for tup in list_of_teams_and_years:
        put_full_roster_in_database(tup[0], tup[1])


if __name__ == "__main__":
    main()
