# get career statistics for a player
# graph the career statistics for a player vs positional groups

# This plot was generated using the rapidAPI data in careerStats table

import matplotlib.pyplot as plt
import rapidAPI as rapidApi

def sort_data_into_positions(results):
    d = {}

    for result in results:
        if result[0] not in d:
            d[result[0]] = []
        d[result[0]].append(result)
    return d

def get_weighted_hitting_averages(position_dict, stats_dict):
    #get weighted averages for each statistic
    #weighted average for home runs is the sum of the homeruns for each player divided by the sum of the number of at bats for each player * 1000 abs
    #weighted average for ops is the sum of the ops statistic times the at_bats for each player divided by the sum of the number of at bats for each player
    #weighted average for era is the sum of the era statistic times innings_pitched for each player divided by the sum of the innings_pitched for each player
    #weighted average for whip is the sum of the whip statistic times innings_pitched for each player divided by the sum of the innings_pitched for each player
    
    for position in position_dict:
        stats_dict[position] = {}
        if position != "P":
            #weighted average for home runs
            total_home_runs = 0
            total_at_bats = 0
            for player in position_dict[position]:
                total_home_runs += player[3]
                total_at_bats += player[1]
            stats_dict[position]["homeruns"] = total_home_runs / total_at_bats * 1000

            #weighted average for ops
            total_ops = 0
            for player in position_dict[position]:
                total_ops += player[2] * player[1]
            stats_dict[position]["ops"] = total_ops / total_at_bats
    return None

def main():
    #get player data from careeer stats table
    connection, cursor = rapidApi.get_connection()
    cursor.execute('SELECT position, at_bats, ops, homeruns, innings_pitched, era, whip FROM CareerStats')
    results = cursor.fetchall() 
    position_dict = sort_data_into_positions(results)
    stats_dict = {}

    for position in position_dict:
        stats_dict[position] = {}
    
    get_weighted_hitting_averages(position_dict, stats_dict)

    #plot 2 graphs next to each other
    #one for home runs, one for ops
    #each graph will have 9 bars, one for each position (DH, C, 1B, 2B, 3B, SS, LF, CF, RF)
    #each bar will be the weighted average for that position
    #each graph will have a title

    fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    fig.suptitle("Weighted Average of Home Runs and OPS for Each Position")
    fig.tight_layout(pad=3.0)

    positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]
    #append homeruns and ops in order of positions
    homeruns = []
    ops = []
    for position in positions:
        homeruns.append(stats_dict[position]["homeruns"])
        ops.append(stats_dict[position]["ops"])
    
    
    axs[0].bar(positions, homeruns)
    axs[0].set_title("Weighted Average of Home Runs")
    axs[0].set_xlabel("positions")
    axs[0].set_ylabel("Home Runs Per 1000 At Bats")
    axs[1].bar(positions, ops)
    axs[1].set_title("Weighted Average of OPS")
    axs[1].set_xlabel("positions")
    axs[1].set_ylabel("OPS")
    plt.show()

    connection.close()

if __name__ == "__main__":
    main()