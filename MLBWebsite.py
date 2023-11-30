#Where all the MLB.com Beautiful Soup scraping is done

from bs4 import BeautifulSoup
import requests
import sqlite3

dates2016WS = ["2016-10-25", "2016-10-26", "2016-10-28", "2016-10-29", "2016-10-30", "2016-11-01", "2016-11-02"]
dates2017WS = ["2017-10-24", "2017-10-25", "2017-10-27", "2017-10-28", "2017-10-29", "2017-10-31", "2017-11-01"]

#create global variable for customGameId
customGameId = 1

def drop_tables():
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS Scores')
    connection.commit()
    connection.close()
    return None

def get_connection():
    connection = sqlite3.connect('baseball.db')
    cursor = connection.cursor()
    return connection, cursor

def put_scores_in_database(list_of_dates):
    #Algorithm:
    #1. get the scores from the MLB.com website
    #2. add the scores to the database (home team, away team, home score, away score, date)

    game = 1
    global customGameId

    for date in list_of_dates:
        url = "https://www.mlb.com/scores/" + date
        
        #connect to beautiful soup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        #get the scores
        table = soup.find("table", {"class": "tablestyle__StyledTable-sc-wsl6eq-0 fxhlOg"})
        tbody = table.find_all("tbody")
        trs = tbody[0].find_all("tr")

        awayDiv = trs[0].find_all("div", {"class": "lineScorestyle__StyledInningCell-sc-1d7bghs-1 ddFUsj"})
        homeDiv = trs[1].find_all("div", {"class": "lineScorestyle__StyledInningCell-sc-1d7bghs-1 jPCzPZ"})

        awayScore = awayDiv[0].text
        homeScore = homeDiv[0].text

        #get the teams
        teams = soup.find_all("div", {"class": "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 fdaoCu"})
        awayTeam = teams[1].text
        homeTeam = teams[0].text

        #print to database with table name "Scores" containing columns "Date", "HomeTeam", "HomeScore", "AwayTeam", "AwayScore"
        ret = get_connection()
        connection = ret[0]
        cursor = ret[1]

        #create if not exists
        cursor.execute('CREATE TABLE IF NOT EXISTS Scores (CustomGameID INTEGER PRIMARY KEY, Year text, Game INTEGER, Date text, HomeTeam text, HomeScore INTEGER, AwayTeam text, AwayScore INTEGER)')
        cursor.execute('INSERT INTO Scores VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (customGameId, date[0:4], game, date, homeTeam, homeScore, awayTeam, awayScore))
        connection.commit()
        connection.close()

        game += 1
        customGameId += 1


    return None
    
def main():
    drop_tables()
    put_scores_in_database(dates2016WS)
    put_scores_in_database(dates2017WS)

if __name__ == "__main__":
    main()