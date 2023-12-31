# Description: This file is used to plot the home and away scores to see if there is a correlation of home field advantage.
# Graph is plotted using matplotlib.
# Runs scored and runs allowed are displayed.

#This plot was generated using the Website

import MLBWebsite as mlbWeb
import matplotlib.pyplot as plt
import driver

list_of_teams_and_years = driver.list_of_teams_and_years

def main():
    connection, cursor = mlbWeb.get_connection()

    teams_to_plot = driver.get_teams_to_plot()


    #for each team, get runs scored and runs allowed on home and away
    cursor.execute('SELECT HomeTeam, HomeScore, AwayTeam, AwayScore FROM Scores')
    scores = cursor.fetchall()

    #output to file
    f = open("output.txt", "a")
    f.write("--- Output for Plot 1 ---\n\n")

    teams = {}
    for score in scores:
        if score[0] in teams_to_plot and score[0] not in teams:
            #home runs, home allowed, away runs, away allowed, games played
            teams[score[0]] = {"runsScoredHome": 0, "runsAllowedHome": 0, "runsScoredAway": 0, "runsAllowedAway": 0, "gamesPlayedHome": 0, "gamesPlayedAway": 0}

    for score in scores:
        if score[0] in teams:
            #home runs, home allowed, away runs, away allowed, games played
            teams[score[0]]["runsScoredHome"] += score[1]
            teams[score[0]]["runsAllowedHome"] += score[3]
            teams[score[0]]["gamesPlayedHome"] += 1
        if score[2] in teams:
            teams[score[2]]["runsScoredAway"] += score[3]
            teams[score[2]]["runsAllowedAway"] += score[1]
            teams[score[2]]["gamesPlayedAway"] += 1

    #create figure to hold all team graphs
    #for each team make 2 bar charts on the same subplot
    #one for runs average scored (home versus away), one for runs average allowed (home versus away), average over length of scores
    #each team will have 2 graphs, title will be team name
    #each graph will have 2 bars, one for home, one for away
    #each graph title will be runs scored or runs allowed
    
    numberOfTeams = len(teams)

    #scale the figure to fit all the graphs
    fig, axs = plt.subplots(numberOfTeams, 2, figsize=(10, 10))
    fig.suptitle("Runs Scored and Allowed Per Game Between Home and Away")
    fig.tight_layout(pad=3.0)

    i = 0
    for team in teams:
        homeRunsScored = teams[team]["runsScoredHome"]
        homeRunsAllowed = teams[team]["runsAllowedHome"]
        awayRunsScored = teams[team]["runsScoredAway"]
        awayRunsAllowed = teams[team]["runsAllowedAway"]
        gamesPlayedHome = teams[team]["gamesPlayedHome"]
        gamesPlayedAway = teams[team]["gamesPlayedAway"]

        runsScored = [homeRunsScored / gamesPlayedHome, awayRunsScored / gamesPlayedAway]
        runsAllowed = [homeRunsAllowed / gamesPlayedHome, awayRunsAllowed / gamesPlayedAway]



        axs[i, 0].bar([1, 2], runsScored, tick_label=["Home", "Away"])
        axs[i, 0].set_title(team + " Playoffs Runs Scored All Time")
        axs[i, 0].set_ylabel("Runs Scored Per Game")

        #set y axis max value to be slitghly above the highest value
        maxVal = max(runsScored)
        axs[i, 0].set_ylim([0, maxVal + 1])


        #put the values right at the top
        for j in range(2):
            height = runsScored[j]
            axs[i, 0].text(j + 1, height, str(round(height, 2)), ha="center", va="bottom")
            

        axs[i, 1].bar([1, 2], runsAllowed, tick_label=["Home", "Away"])
        axs[i, 1].set_title(team + " Playoffs Runs Allowed All Time")
        axs[i, 1].set_ylabel("Runs Allowed Per Game")

        #set y axis max value to be slitghly above the highest value
        maxVal = max(runsAllowed)
        axs[i, 1].set_ylim([0, maxVal + 1])

        for j in range(2):
            height = runsAllowed[j]
            axs[i, 1].text(j + 1, height, str(round(height, 2)), ha="center", va="bottom")

        i += 1
        
        #round values to 2 decimal places
        runsScored[0] = round(runsScored[0], 2)
        runsScored[1] = round(runsScored[1], 2)
        runsAllowed[0] = round(runsAllowed[0], 2)
        runsAllowed[1] = round(runsAllowed[1], 2)
        f.write(team + " Playoffs Runs Scored At Home Per Game: " + str(runsScored[0]) + "\n")
        f.write(team + " Playoffs Runs Scored On Road Per Game: " + str(runsScored[1]) + "\n")
        f.write(team + " Playoffs Runs Allowed At Home Per Game: " + str(runsAllowed[0]) + "\n")
        f.write(team + " Playoffs Runs Allowed On Road Per Game: " + str(runsAllowed[1]) + "\n")
        f.write("\n")
        
    f.write("--- End Output for Plot 1 ---\n\n")
    f.close()
    plt.show()
    return None




    connection.close()




if __name__ == "__main__":
    main()