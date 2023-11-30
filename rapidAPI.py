#Everything to do with the Rapid API calls
#Uses rapid api for career stats and number of teams played for

import requests

url_player_info_rapid = "https://mlb-data.p.rapidapi.com/json/named.player_info.bam"

### Printing Functions ###

def print_player_info(filename, player_info):
    f = open(filename, "w")
    f.write(str(player_info))
    f.close()
    return None


### API Calls ###

def get_api_full_info(url, input_headers, input_params):
    response = requests.get(url, headers=input_headers, params=input_params)
    return response.json()

def handle_player_info():
    player_id = "493316"
    querystring_Rapid = {"sport_code":"'mlb'", "player_id":player_id} #can loop through players like that
    headers_Rapid = {
        "X-RapidAPI-Key": "0e16a7778fmsh307708c41723323p11dd1cjsn85e69ae1746e",
        "X-RapidAPI-Host": "mlb-data.p.rapidapi.com"
    }
    response_player_info = get_api_full_info(url_player_info_rapid, headers_Rapid, querystring_Rapid)
    print_player_info("output_player.txt", response_player_info)
    return None


### MISCELLANEOUS ###

def main():
    #Algorithm:
    #1. get a couple players from rapid API
    #2. add career stats to database
    #3. add number of teams played for to database
    pass

if __name__ == "__main__":
    main()