#Where all the MLB.com Beautiful Soup scraping is done

from bs4 import BeautifulSoup
import requests
import sqlite3
import driver

series_to_scrape = driver.series_to_scrape
num_games_to_scrape = driver.num_games_to_scrape

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
        customGameId = int(date[0:4] + date[5:7] + date[8:10])

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