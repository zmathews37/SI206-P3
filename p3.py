import requests

url_player_info_rapid = "https://mlb-data.p.rapidapi.com/json/named.player_info.bam"
urlbaseMLB = "http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2017'"

headers_Rapid = {
    "X-RapidAPI-Key": "0e16a7778fmsh307708c41723323p11dd1cjsn85e69ae1746e",
    "X-RapidAPI-Host": "mlb-data.p.rapidapi.com"
}

def get_info_from_api(url, input_headers, input_params):
    response = requests.get(url, headers=input_headers, params=input_params)
    return response.json()

def print_player_info(filename, player_info):
    f = open(filename, "w")
    f.write(str(player_info))
    f.close()

def print_team_info(filename, team_info):
    f = open(filename, "w")
    teams = team_info["team_all_season"]["queryResults"]["row"]
    for team in teams:
        f.write(str(team))
        f.write("\n")
    f.close()

def main():
    player_id = "493316"
    querystring_Rapid = {"sport_code":"'mlb'", "player_id":player_id} #can loop through players like that
    response_player_info = get_info_from_api(url_player_info_rapid, headers_Rapid, querystring_Rapid)
    response_team_info = get_info_from_api(urlbaseMLB, None, None)

    #print contents
    print_player_info("output_player.txt", response_player_info)
    print_team_info("output_team.txt", response_team_info)



if __name__ == "__main__":
    main()