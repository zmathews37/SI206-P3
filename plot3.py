# This plot was generated using the mlbAPI data in Statistics table and Players table 
# This is where join was used

import matplotlib.pyplot as plt
import mlbAPI as mlb

def join_tables():
    connection, cursor = mlb.get_connection()
    cursor.execute('SELECT position, at_bats, ops, homeruns, innings_pitched, era, whip FROM Statistics JOIN Players ON Statistics.player_id = Players.player_id')
    results = cursor.fetchall()
    connection.close()
    return results



def main():
    #get the data
    results = join_tables()




if __name__ == "__main__":
    main()