import matplotlib.pyplot as plt
import numpy as np
import MLBWebsite as mlbWeb

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
    f.write("\n")
    f.close()

    #plot the margin of victory as side by side bar graph
    plt.bar([1, 2], [homeMarginAvg, awayMarginAvg], tick_label=["Home Win", "Away Win"])
    plt.title("Margin of Victory")
    plt.ylabel("Average Margin of Victory (runs)")
    plt.show()
    return None

def main():
    connection, cursor = mlbWeb.get_connection()
    plot_margin_of_victory(connection, cursor)
    connection.close()
    return None

if __name__ == "__main__":
    main()