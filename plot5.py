import matplotlib.pyplot as plt
import MLBWebsite as mlbWeb
import driver

list_of_teams_and_years = driver.list_of_teams_and_years

def plot_run_differentials(connection, cursor):
    #print to output
    f = open("output.txt", "a")
    f.write("--- Output for Plot 5 ---\n\n")
    f.write("Run Differentials For Each Game:\n\n")
    teams_to_plot = driver.get_teams_to_plot()

    cursor.execute('SELECT HomeTeam, AwayTeam, HomeScore, AwayScore, year FROM Scores')
    scores = cursor.fetchall()
    runDifferentials = {}

    f.write("Home Team - Away Team (Year)" + "\tDifferential = Home Score - Away Score" "\n")
    for score in scores:
        home_team, away_team = score[0], score[1]
        run_diff = score[2] - score[3]

        f.write(home_team + " " + str(score[2]) + " - " + str(score[3]) + " " + away_team + " (" + str(score[4]) + ")" + "   Differential = " + str(run_diff) + "\n")

        if home_team in teams_to_plot:
            # Initialize dictionaries for each team if not present
            if home_team not in runDifferentials:
                runDifferentials[home_team] = []
            # Append run differentials to respective teams
            runDifferentials[home_team].append(run_diff)

        if away_team in teams_to_plot:
            # Initialize dictionaries for each team if not present
            if away_team not in runDifferentials:
                runDifferentials[away_team] = []
            # Append run differentials to respective teams
            runDifferentials[away_team].append(-run_diff)  # Negative for away teams


    f.write("\n\nRun Differentials Distribution for Each Team\n\n")
    for team in runDifferentials:
        f.write(team + ": " + str(runDifferentials[team]) + "\n")
    
    f.write("\n")
    f.write("--- End Output for Plot 5 ---\n\n")


    # Plot histogram for run differentials
    plt.figure(figsize=(12, 6))
    plt.hist(runDifferentials.values(), bins=20, alpha=0.7, edgecolor='black', linewidth=1.2)
    plt.title("Run Differentials Distribution for Each Team")
    plt.xlabel("Run Differential (Runs Scored - Runs Allowed)")
    plt.ylabel("Frequency")
    plt.grid(True)


    #add legend
    legend = list(runDifferentials.keys())
    plt.legend(legend)
    plt.show()

    return None

def main():
    connection, cursor = mlbWeb.get_connection()
    plot_run_differentials(connection, cursor)
    connection.close()

if __name__ == "__main__":
    main()
