import matplotlib.pyplot as plt
import MLBWebsite as mlbWeb

def plot_run_differentials(connection, cursor):
    cursor.execute('SELECT HomeTeam, AwayTeam, HomeScore, AwayScore, year FROM Scores')
    scores = cursor.fetchall()
    legend = []
    d = {}

    runDifferentials = {}

    for score in scores:
        home_team, away_team = score[0], score[1]
        run_diff = score[2] - score[3]

        # Initialize dictionaries for each team if not present
        if home_team not in runDifferentials:
            runDifferentials[home_team] = []
        if away_team not in runDifferentials:
            runDifferentials[away_team] = []

        # Append run differentials to respective teams
        runDifferentials[home_team].append(run_diff)
        runDifferentials[away_team].append(-run_diff)  # Negative for away teams

        if home_team not in d:
            d[home_team] = []
            legend.append(home_team + " " + str(score[4]))


    # Plot histogram for run differentials
    plt.figure(figsize=(12, 6))
    plt.hist(runDifferentials.values(), bins=20, alpha=0.7, edgecolor='black', linewidth=1.2)
    plt.title("Run Differentials Distribution for Each Team")
    plt.xlabel("Run Differential (Runs Scored - Runs Allowed)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)


    #add legend
    plt.legend(legend)

    plt.show()

    return None

def main():
    connection, cursor = mlbWeb.get_connection()
    plot_run_differentials(connection, cursor)
    connection.close()

if __name__ == "__main__":
    main()
