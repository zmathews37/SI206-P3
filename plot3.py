# This plot was generated using the mlbAPI data in Statistics table and Players table 
# This is where join was used
# Comparing the weighted averages of the playoff teams

import matplotlib.pyplot as plt
import mlbAPI as mlb
import driver

list_of_teams_and_years = driver.list_of_teams_and_years

def join_tables(team1, team2, team3, team4):
    connection, cursor = mlb.get_connection()
    #join on id AND team_id
    #where team and year are the same
    #team1

    team1Name, team1Year = team1
    team2Name, team2Year = team2
    team3Name, team3Year = team3
    team4Name, team4Year = team4

    results = []
    cursor.execute('SELECT team_name, position, at_bats, ops, homeruns, innings_pitched, era, whip FROM Players JOIN Statistics ON Players.player_id = Statistics.player_id WHERE Players.team_name = ? AND Players.year = ?', (team1Name, team1Year))
    results.extend(cursor.fetchall())
    cursor.execute('SELECT team_name, position, at_bats, ops, homeruns, innings_pitched, era, whip FROM Players JOIN Statistics ON Players.player_id = Statistics.player_id WHERE Players.team_name = ? AND Players.year = ?', (team2Name, team2Year))
    results.extend(cursor.fetchall())
    cursor.execute('SELECT team_name, position, at_bats, ops, homeruns, innings_pitched, era, whip FROM Players JOIN Statistics ON Players.player_id = Statistics.player_id WHERE Players.team_name = ? AND Players.year = ?', (team3Name, team3Year))
    results.extend(cursor.fetchall())
    cursor.execute('SELECT team_name, position, at_bats, ops, homeruns, innings_pitched, era, whip FROM Players JOIN Statistics ON Players.player_id = Statistics.player_id WHERE Players.team_name = ? AND Players.year = ?', (team4Name, team4Year))
    results.extend(cursor.fetchall())

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

    team1Tup = list_of_teams_and_years[0]
    team2Tup = list_of_teams_and_years[1]
    team3Tup = list_of_teams_and_years[2]
    team4Tup = list_of_teams_and_years[3]

    results = join_tables(team1Tup, team2Tup, team3Tup, team4Tup)
    team1_players = []
    team2_players = []
    team3_players = []
    team4_players = []

    team1Name = team1Tup[0]
    team2Name = team2Tup[0]
    team3Name = team3Tup[0]
    team4Name = team4Tup[0]

    #sort the data into dictionaries
    for player in results:
        if player[0] == team1Name:
            team1_players.append(player)
        elif player[0] == team2Name:
            team2_players.append(player)
        elif player[0] == team3Name:
            team3_players.append(player)
        elif player[0] == team4Name:
            team4_players.append(player)
    


    team1_ops, team1_homeruns, team1_era, team1_whip = get_team_stats(team1_players)
    team2_ops, team2_homeruns, team2_era, team2_whip = get_team_stats(team2_players)
    team3_ops, team3_homeruns, team3_era, team3_whip = get_team_stats(team3_players)
    team4_ops, team4_homeruns, team4_era, team4_whip = get_team_stats(team4_players)

    data_list.append([team1_ops, team1_homeruns, team1_era, team1_whip])
    data_list.append([team2_ops, team2_homeruns, team2_era, team2_whip])
    data_list.append([team3_ops, team3_homeruns, team3_era, team3_whip])
    data_list.append([team4_ops, team4_homeruns, team4_era, team4_whip])

    #for each stat, plot every team with different colors
    #each bar has a different color
    #plot on same figure, different 4 subplots with each stat
    #add different colors for each team

    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Comparing Team Stats of World Series teams')
    fig.tight_layout(pad=0.5)

    #OPS
    axs[0, 0].bar([team1Name, team2Name, team3Name, team4Name], [team1_ops, team2_ops, team3_ops, team4_ops], color=['red', 'blue', 'green', 'purple'])
    axs[0, 0].set_title('OPS')
    axs[0, 0].set_ylabel('OPS')

    #Home Runs
    axs[0, 1].bar([team1Name, team2Name, team3Name, team4Name], [team1_homeruns, team2_homeruns, team3_homeruns, team4_homeruns], color=['red', 'blue', 'green', 'purple'])
    axs[0, 1].set_title('Home Runs')
    axs[0, 1].set_ylabel('Home Runs')

    #ERA
    axs[1, 0].bar([team1Name, team2Name, team3Name, team4Name], [team1_era, team2_era, team3_era, team4_era], color=['red', 'blue', 'green', 'purple'])
    axs[1, 0].set_title('ERA')
    axs[1, 0].set_ylabel('ERA')

    #WHIP
    axs[1, 1].bar([team1Name, team2Name, team3Name, team4Name], [team1_whip, team2_whip, team3_whip, team4_whip], color=['red', 'blue', 'green', 'purple'])
    axs[1, 1].set_title('WHIP')
    axs[1, 1].set_ylabel('WHIP')


    #print the data
    #connect output file
    f = open("output.txt", "a")
    f.write("--- Output for Plot 3 ---\n\n")
    f.write("Comparing Team Stats of World Series teams\n\n")

    f.write("OPS\n")
    f.write(team1Name + ": " + str(round(team1_ops, 3)) + "\n")
    f.write(team2Name + ": " + str(round(team2_ops, 3)) + "\n")
    f.write(team3Name + ": " + str(round(team3_ops, 3)) + "\n")
    f.write(team4Name + ": " + str(round(team4_ops, 3)) + "\n\n")


    f.write("Home Runs\n")
    f.write(team1Name + ": " + str(round(team1_homeruns, 3)) + "\n")
    f.write(team2Name + ": " + str(round(team2_homeruns, 3)) + "\n")
    f.write(team3Name + ": " + str(round(team3_homeruns, 3)) + "\n")
    f.write(team4Name + ": " + str(round(team4_homeruns, 3)) + "\n\n")

    f.write("ERA\n")
    f.write(team1Name + ": " + str(round(team1_era, 2)) + "\n")
    f.write(team2Name + ": " + str(round(team2_era, 2)) + "\n")
    f.write(team3Name + ": " + str(round(team3_era, 2)) + "\n")
    f.write(team4Name + ": " + str(round(team4_era, 2)) + "\n\n")

    f.write("WHIP\n")
    f.write(team1Name + ": " + str(round(team1_whip, 2)) + "\n")
    f.write(team2Name + ": " + str(round(team2_whip, 2)) + "\n")
    f.write(team3Name + ": " + str(round(team3_whip, 2)) + "\n")
    f.write(team4Name + ": " + str(round(team4_whip, 2)) + "\n\n")

    f.write("--- End Output for Plot 3 ---\n\n")
    f.close()

    plt.show()




if __name__ == "__main__":
    main()