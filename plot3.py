# This plot was generated using the mlbAPI data in Statistics table and Players table 
# This is where join was used
# Comparing the weighted averages of the playoff teams

import matplotlib.pyplot as plt
import mlbAPI as mlb

team1 = "Houston Astros"
team2 = "Los Angeles Dodgers"
team3 = "San Francisco Giants"
team4 = "Detroit Tigers"

matchups = [(team1, team2), (team3, team4)]

def join_tables(team1, team2):
    connection, cursor = mlb.get_connection()
    #join on id AND team_id
    cursor.execute('SELECT team_name, position, at_bats, ops, homeruns, innings_pitched, era, whip FROM Statistics JOIN Players ON Statistics.player_id = Players.player_id WHERE Players.team_name = ? OR Players.team_name = ?', (team1, team2))
    results = cursor.fetchall()
    connection.close()
    return results

def get_team_stats(player_list):
    team_ops = 0
    team_era = 0
    team_homeruns = 0
    team_whip = 0

    for player in player_list:
        if player[1] != "P":
            team_ops += player[3] * player[2]
            team_homeruns += player[4]
        else:
            team_era += player[6] * player[5]
            team_whip += player[7] * player[5]

    team_ops = team_ops / sum(player[2] for player in player_list if player[1] != "P")
    team_era = team_era / sum(player[5] for player in player_list if player[1] == "P")
    team_whip = team_whip / sum(player[5] for player in player_list if player[1] == "P")
    return team_ops, team_homeruns, team_era, team_whip


def main():
    #get the data for each matchup
    data_list = []

    for matchup in matchups:
        team1 = matchup[0]
        team2 = matchup[1]

        results = join_tables(team1, team2)
        team1_players = []
        team2_players = []

        #sort the data into two dictionaries
        for player in results:
            if player[0] == team1:
                team1_players.append(player)
            else:
                team2_players.append(player)

        team1_ops, team1_homeruns, team1_era, team1_whip = get_team_stats(team1_players)
        team2_ops, team2_homeruns, team2_era, team2_whip = get_team_stats(team2_players)

        data_list.append([team1_ops, team1_homeruns, team1_era, team1_whip])
        data_list.append([team2_ops, team2_homeruns, team2_era, team2_whip])

    #plot the data
    fig, ax = plt.subplots(2, 2)
    fig.suptitle('Comparing the weighted averages of World Series teams')
    fig.tight_layout(pad=0.5)

    #for each stat, plot every team with different colors
    #each bar has a different color

    #OPS
    ax[0, 0].bar([matchups[0][0], matchups[0][1]], [data_list[0][0], data_list[1][0]], color=["blue", "orange"])
    ax[0, 0].bar([matchups[1][0], matchups[1][1]], [data_list[2][0], data_list[3][0]], color=["green", "red"])
    ax[0, 0].set_title("OPS")
    ax[0, 0].set_ylabel("OPS")

    #Home Runs
    ax[0, 1].bar([matchups[0][0], matchups[0][1]], [data_list[0][1], data_list[1][1]], color=["blue", "orange"])
    ax[0, 1].bar([matchups[1][0], matchups[1][1]], [data_list[2][1], data_list[3][1]], color=["green", "red"])
    ax[0, 1].set_title("Home Runs")
    ax[0, 1].set_ylabel("Home Runs")

    #ERA
    ax[1, 0].bar([matchups[0][0], matchups[0][1]], [data_list[0][2], data_list[1][2]], color=["blue", "orange"])
    ax[1, 0].bar([matchups[1][0], matchups[1][1]], [data_list[2][2], data_list[3][2]], color=["green", "red"])
    ax[1, 0].set_title("ERA")
    ax[1, 0].set_ylabel("ERA")

    #WHIP
    ax[1, 1].bar([matchups[0][0], matchups[0][1]], [data_list[0][3], data_list[1][3]], color=["blue", "orange"])
    ax[1, 1].bar([matchups[1][0], matchups[1][1]], [data_list[2][3], data_list[3][3]], color=["green", "red"])
    ax[1, 1].set_title("WHIP")
    ax[1, 1].set_ylabel("WHIP")

    #print the data
    #connect output file
    f = open("output.txt", "a")
    f.write("--- Output for Plot 3 ---\n\n")
    f.write("Comparing the weighted averages of World Series teams\n\n")

    f.write("OPS\n")
    f.write(matchups[0][0] + ": " + str(round(data_list[0][0], 3)) + "\n")
    f.write(matchups[0][1] + ": " + str(round(data_list[1][0], 3)) + "\n")
    f.write(matchups[1][0] + ": " + str(round(data_list[2][0], 3)) + "\n")
    f.write(matchups[1][1] + ": " + str(round(data_list[3][0], 3)) + "\n\n")

    f.write("Home Runs\n")
    f.write(matchups[0][0] + ": " + str(data_list[0][1]) + "\n")    
    f.write(matchups[0][1] + ": " + str(data_list[1][1]) + "\n")
    f.write(matchups[1][0] + ": " + str(data_list[2][1]) + "\n")
    f.write(matchups[1][1] + ": " + str(data_list[3][1]) + "\n\n")

    f.write("ERA\n")
    f.write(matchups[0][0] + ": " + str(round(data_list[0][2], 2)) + "\n")
    f.write(matchups[0][1] + ": " + str(round(data_list[1][2], 2)) + "\n")
    f.write(matchups[1][0] + ": " + str(round(data_list[2][2], 2)) + "\n")
    f.write(matchups[1][1] + ": " + str(round(data_list[3][2], 2)) + "\n\n")

    f.write("WHIP\n")
    f.write(matchups[0][0] + ": " + str(round(data_list[0][3], 2)) + "\n")
    f.write(matchups[0][1] + ": " + str(round(data_list[1][3], 2)) + "\n")
    f.write(matchups[1][0] + ": " + str(round(data_list[2][3], 2)) + "\n")
    f.write(matchups[1][1] + ": " + str(round(data_list[3][3], 2)) + "\n\n")
    f.write("--- End Output for Plot 3 ---\n\n")
    f.close()

    plt.show()




if __name__ == "__main__":
    main()