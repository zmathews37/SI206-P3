#Where all the MLB.com Beautiful Soup scraping is done

from bs4 import BeautifulSoup
import requests
import sqlite3

# dates2012ALDS = ["2012-10-06", "2012-10-07", "2012-10-09", "2012-10-10", "2012-10-11"]
# dates2012ALCS = ["2012-10-13", "2012-10-14", "2012-10-16", "2012-10-17", "2012-10-18"]
# dates2012NLDS = ["2012-10-06", "2012-10-07", "2012-10-09", "2012-10-10", "2012-10-11"]
# dates2012NLCS = ["2012-10-14", "2012-10-15", "2012-10-17", "2012-10-18", "2012-10-19"]
dates2012WS   = ["2012-10-24", "2012-10-25", "2012-10-27", "2012-10-28"]
# dates2017ALDS = ["2017-10-05", "2017-10-06", "2017-10-08", "2017-10-09", "2017-10-11", "2017-10-12"]
# dates2017ALCS = ["2017-10-13", "2017-10-14", "2017-10-16", "2017-10-17", "2017-10-18", "2017-10-20", "2017-10-21"]
# dates2017NLDS = ["2017-10-06", "2017-10-07", "2017-10-09", "2017-10-10", "2017-10-11", "2017-10-12"]
# dates2017NLCS = ["2017-10-14", "2017-10-15", "2017-10-17", "2017-10-18", "2017-10-19", "2017-10-21", "2017-10-22"]
dates2017WS   = ["2017-10-24", "2017-10-25", "2017-10-27", "2017-10-28", "2017-10-29", "2017-10-31", "2017-11-01"]
#dates_to_scrape = dates2012ALDS + dates2012ALCS + dates2012NLDS + dates2012NLCS + dates2012WS + dates2017ALDS + dates2017ALCS + dates2017NLDS + dates2017NLCS + dates2017WS
#dates_to_scrape = [dates2012ALDS, dates2012WS, dates2017WS]
series_to_scrape = [dates2012WS, dates2017WS]

num_games_to_scrape = 24

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

def put_scores_in_database(list_of_dates, iterator):
    #Algorithm:
    #1. get the scores from the MLB.com website
    #2. add the scores to the database (home team, away team, home score, away score, date)

    game = 1 #tracks the game number in the series

    for date in list_of_dates:
        url = "https://www.mlb.com/scores/" + date
        customGameId = int(date[0:4] + date[5:7] + date[8:10] + str(game))

        #check if the game exists in the database
        connection, cursor = get_connection()
        cursor.execute('SELECT * FROM Scores WHERE CustomGameID = ?', (customGameId,))
        results = cursor.fetchall()
        connection.close()

        if len(results) > 0: #game already exists in database
            continue
        
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
        awayTeam = teams[0].text
        homeTeam = teams[1].text

        #print to database with table name "Scores" containing columns "Date", "HomeTeam", "HomeScore", "AwayTeam", "AwayScore"
        #key is not team name because there are multiple games with the same teams
        connection, cursor = get_connection()
        cursor.execute('INSERT INTO Scores VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (customGameId, date[0:4], game, date, homeTeam, homeScore, awayTeam, awayScore))
        connection.commit()
        connection.close()

        game += 1
        iterator += 1

        if iterator == num_games_to_scrape:
            return False, iterator
    return True, iterator

    
def main():
    drop_tables()
    connection, cursor = get_connection()
    cursor.execute('CREATE TABLE IF NOT EXISTS Scores (CustomGameID INTEGER PRIMARY KEY, Year text, Game INTEGER, Date text, HomeTeam text, HomeScore INTEGER, AwayTeam text, AwayScore INTEGER)')
    connection.commit()
    connection.close()

    iterator = 0
    for date_list in series_to_scrape:
        continue_scraping, iterator = put_scores_in_database(date_list, iterator)

        if continue_scraping == False:
            return None
    
    print("Done scraping all dates!")

if __name__ == "__main__":
    main()