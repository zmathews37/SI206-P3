# Description: This file is used to plot the home and away scores to see if there is a correlation of home field advantage.
# Graph is plotted using matplotlib.
# Margin of victory is displayed.
# Runs scored and runs allowed are displayed on second graph.

import MLBWebsite as mlb
import matplotlib.pyplot as plt
import numpy as np

def plot_margin_of_victory(connection, cursor):
    cursor.execute('SELECT HomeScore, AwayScore FROM Scores')
    scores = cursor.fetchall()

    homeMargin = []
    awayMargin = []

    for score in scores:
        if score[0] > score[1]:
            homeMargin.append(score[0] - score[1])
        else:
            awayMargin.append(score[1] - score[0])

    homeMarginAvg = np.mean(homeMargin)
    awayMarginAvg = np.mean(awayMargin)

    #create output file
    f = open("output.txt", "w")
    f.write("Home Margin Average: " + str(homeMarginAvg) + "\n")
    f.write("Away Margin Average: " + str(awayMarginAvg) + "\n")
    f.close()

    #plot the margin of victory as side by side bar graph
    plt.bar([1, 2], [homeMarginAvg, awayMarginAvg], tick_label=["Home", "Away"])
    plt.title("Margin of Victory")
    plt.xlabel("Home/Away")
    plt.ylabel("Margin of Victory")
    plt.show()
    return None

def plot_runs_scored_versus_allowed(cursor):
    #for each team, get runs scored and runs allowed on home and away
    cursor.execute('SELECT HomeTeam, HomeScore, AwayTeam, AwayScore FROM Scores')
    scores = cursor.fetchall()

    #output to file
    f = open("output.txt", "a")
    f.write("--- Output for Plot 1 ---\n\n")

    teams = {}
    for score in scores:
        if score[0] not in teams:
            teams[score[0]] = [0, 0, 0, 0, 0] #home runs, home allowed, away runs, away allowed, games played


    for score in scores:
        if score[0] in teams:
            teams[score[0]][0] += score[1] #home runs scored
            teams[score[0]][1] += score[3] #home allowed
            teams[score[2]][2] += score[3] #away runs scored
            teams[score[2]][3] += score[1] #away allowed
            teams[score[0]][4] += 1 #games played
            teams[score[2]][4] += 1 #games played

    #create figure to hold all team graphs
    #for each team make 2 bar charts on the same subplot
    #one for runs average scored (home versus away), one for runs average allowed (home versus away), average over length of scores
    #each team will have 2 graphs, title will be team name
    #each graph will have 2 bars, one for home, one for away
    #each graph title will be runs scored or runs allowed
    
    numberOfTeams = len(teams)

    #scale the figure to fit all the graphs
    fig, axs = plt.subplots(numberOfTeams, 2, figsize=(10, 10))
    fig.suptitle("Runs Score and Allowed Per Game Between Home and Away")
    fig.tight_layout(pad=3.0)

    i = 0
    for team in teams:
        runsScored = [teams[team][0], teams[team][2]]
        runsAllowed = [teams[team][1], teams[team][3]]
        gamesPlayed = teams[team][4]

        runsScored = [x / gamesPlayed for x in runsScored]
        runsAllowed = [x / gamesPlayed for x in runsAllowed]

        axs[i, 0].bar([1, 2], runsScored, tick_label=["Home", "Away"])
        axs[i, 0].set_title(team + " Runs Scored")
        axs[i, 0].set_ylabel("Runs Scored Per Game")

        axs[i, 1].bar([1, 2], runsAllowed, tick_label=["Home", "Away"])
        axs[i, 1].set_title(team + " Runs Allowed")
        axs[i, 1].set_ylabel("Runs Allowed Per Game")

        i += 1
        
        f.write(team + " Runs Scored At Home Per Game: " + str(runsScored[0]) + "\n")
        f.write(team + " Runs Scored On Road Per Game: " + str(runsScored[1]) + "\n")
        f.write(team + " Runs Allowed At Home Per Game: " + str(runsAllowed[0]) + "\n")
        f.write(team + " Runs Allowed On Road Per Game: " + str(runsAllowed[1]) + "\n")
        f.write("\n")
        
    f.write("--- End Output for Plot 1 ---\n\n")
    f.close()
    plt.show()
    return None



def main():
    ret = mlb.get_connection()
    connection = ret[0]
    cursor = ret[1]

    #plot_margin_of_victory(connection, cursor) #unsure if we want to keep this

    #plot runs scored and runs allowed on same figure, different graph
    plot_runs_scored_versus_allowed(cursor)
    connection.close()




if __name__ == "__main__":
    main()