import matplotlib.pyplot as plt
import numpy as np
import MLBWebsite as mlbWeb

def main():
    connection, cursor = mlbWeb.get_connection()
    cursor.execute('SELECT Game, HomeScore, AwayScore FROM Scores')
    scores = cursor.fetchall()

    #create output file
    f = open("output.txt", "w")
    f.write("--- Output for Plot 4 ---\n\n")

    runs_scored_home = {}
    runs_scored_away = {}
    average_home_runs_scored = {}
    average_away_runs_scored = {}

    for i in range(1, 8):
        runs_scored_home[i] = []
        runs_scored_away[i] = []
        average_home_runs_scored[i] = 0
        average_away_runs_scored[i] = 0

    #get runs scored for each game of the series, 1, 2, 3, 4, 5, 6, 7
    for score in scores:
        game = score[0]
        home_score = score[1]
        away_score = score[2]

        runs_scored_home[game].append(home_score)
        runs_scored_away[game].append(away_score)

    #get average runs scored for each game
    for game in runs_scored_home:
        average_home_runs_scored[game] = np.mean(runs_scored_home[game])
        average_away_runs_scored[game] = np.mean(runs_scored_away[game])
    
    #plot the data side by side same bar chart, no subplots
    #side by side not stacked
    #each xtick contains both home and away
    #xlabel should be between the two bars

    fig, ax = plt.subplots()
    fig.suptitle("Average Runs Scored Per Game")
    fig.tight_layout(pad=3.0)

    #set width of bar
    barWidth = 0.25

    #set height of bar
    home = []
    away = []
    for i in range(1, 8):
        home.append(average_home_runs_scored[i])
        away.append(average_away_runs_scored[i])
    
    #set position of bar on x axis
    r1 = np.arange(len(home))
    r2 = [x + barWidth for x in r1]

    #make the plot
    plt.bar(r1, home, color="blue", width=barWidth, edgecolor="white", label="Home Runs Scored")
    plt.bar(r2, away, color="orange", width=barWidth, edgecolor="white", label="Away Runs Scored")


    #add xticks on the middle of the group bars
    plt.xlabel("Game of World Series (1-7)")
    plt.ylabel("Average Runs Scored Per Game")
    plt.xticks([r + barWidth/2 for r in range(len(home))], ["1", "2", "3", "4", "5", "6", "7"])

    #create legend and show plot
    plt.legend()

    

    #print the data
    #use rounding
    f.write("Average Runs Scored Per Game\n")
    f.write("In Game 1's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[1], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[1], 2)) + "\n\n")
    f.write("In Game 2's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[2], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[2], 2)) + "\n\n")
    f.write("In Game 3's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[3], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[3], 2)) + "\n\n")
    f.write("In Game 4's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[4], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[4], 2)) + "\n\n")
    f.write("In Game 5's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[5], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[5], 2)) + "\n\n")
    f.write("In Game 6's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[6], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[6], 2)) + "\n\n")
    f.write("In Game 7's: \n")
    f.write("Home: " + str(round(average_home_runs_scored[7], 2)) + "\n")
    f.write("Away: " + str(round(average_away_runs_scored[7], 2)) + "\n\n")


    f.write("--- End Output for Plot 4 ---\n\n")

    plt.show()
    connection.close()

    return None

if __name__ == "__main__":
    main()