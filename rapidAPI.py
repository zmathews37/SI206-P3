# Everything to do with the Rapid API calls
# Uses rapid api for career stats and career games played
# Make a weighted average for some positions

import requests
import sqlite3

urlSeason = "https://mlb-data.p.rapidapi.com/json/named.team_all_season.bam"
querystringSeason = {"season":"'2017'","all_star_sw":"'N'","sort_order":"name_asc"}

urlRoster = "https://mlb-data.p.rapidapi.com/json/named.roster_team_alltime.bam"
querystringRoster = {"end_season":"'2017'","team_id":"'121'","start_season":"'2017'","all_star_sw":"'N'","sort_order":"name_asc"}

urlCareerPitcher = "https://mlb-data.p.rapidapi.com/json/named.sport_career_pitching.bam"
querystringCareer = {"player_id":"'592789'","league_list_id":"'mlb'","game_type":"'R'"}
urlCareerHitter = "https://mlb-data.p.rapidapi.com/json/named.sport_career_hitting.bam"

headers = {
	"X-RapidAPI-Key": "0e16a7778fmsh307708c41723323p11dd1cjsn85e69ae1746e",
	"X-RapidAPI-Host": "mlb-data.p.rapidapi.com"
}

list_of_teams_and_years = [("San Francisco Giants", "2012"), ("Detroit Tigers", "2012"), ("Houston Astros", "2017"), ("Los Angeles Dodgers", "2017")]

### FUNCTIONS ###

def get_roster(team_name, year, teamsDict):
    team_id = teamsDict[team_name]
    querystringRoster["start_season"] = "'" + year + "'"
    querystringRoster["end_season"] = "'" + year + "'"
    querystringRoster["team_id"] = "'" + team_id + "'"
    response = requests.get(urlRoster, headers=headers, params=querystringRoster)
    data = response.json()
    return data["roster_team_alltime"]["queryResults"]["row"]

def get_career_stats(player_id, pitcher):
    if pitcher:
        urlCareer = urlCareerPitcher
    else:
        urlCareer = urlCareerHitter

    querystringCareer["player_id"] = "'" + player_id + "'"
    response = requests.get(urlCareer, headers=headers, params=querystringCareer).json()
    
    if pitcher:
        return response["sport_career_pitching"]["queryResults"]["row"]
    else:
        return response["sport_career_hitting"]["queryResults"]["row"]



### MISCELLANEOUS ###

def store_teams_dict():
    d = {}
    info = requests.get(urlSeason, headers=headers, params=querystringSeason).json()
    teams = info["team_all_season"]["queryResults"]["row"]

    for team in teams:
        d[team["name_display_full"]] = team["team_id"]
    return d


#only use when needed!!!
def drop_tables(): 
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS CareerStats')
    connection.commit()
    connection.close()
    return None

def get_connection():
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    return connection, cursor

def put_player_in_career_stats_table(player_id, player_name, ops, homerun, era, whip):
    connection, cursor = get_connection()
    cursor.execute('CREATE TABLE IF NOT EXISTS CareerStats (PlayerID INTEGER PRIMARY KEY, Name text, OPS REAL, Homerun INTEGER, ERA REAL, WHIP REAL)')
    cursor.execute('INSERT INTO CareerStats VALUES (?, ?, ?, ?, ?, ?)', (player_id, player_name, ops, homerun, era, whip))
    connection.commit()
    connection.close()
    return None

def main():
    #Algorithm:
    #1. get a couple players from rapid API
    #2. add career stats to database
    #3. add number of teams played for to database
    drop_tables()
    teamsDict = store_teams_dict()

    for team in list_of_teams_and_years:
        roster = get_roster(team[0], team[1], teamsDict)
        for player in roster:
            name = player["name_first_last"]
            player_id_db = int(player["player_id"] + team[1])

            player_stats = get_career_stats(player["player_id"], player["position_desig"] == "PITCHER")

            if player["position_desig"] == "PITCHER":
                era = player_stats["era"]
                whip = player_stats["whip"]
                put_player_in_career_stats_table(player_id_db, name, None, None, era, whip)
            else:
                ops = player_stats["ops"]
                homerun = player_stats["hr"]
                put_player_in_career_stats_table(player_id_db, name, ops, homerun, None, None)


if __name__ == "__main__":
    main()