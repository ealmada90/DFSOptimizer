import csv
from DFSPlayer import *
from pulp import *

#declare variables
lineupSlots = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
positionRequirements = ["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"]

#declare functions
def create_player_from_row(row):
    return DFSPlayer(row['Name'], row['Team'], row['Position'], int(row['Salary']), float(row['Projected']))

def read_csv(file_path):
    players = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = create_player_from_row(row=row)
            if(player.projection > 0):
                players.append(player)
    return players

def initPlayerContainers(list):
    for slot,players in lineupSlots.items():
        for player in list:
            if(positionRequirements[slot] in player.position):
                players.append(player)


def initTeamList(list):
    teamList = []
    for player in list:
        if(player.team not in teamList):
            teamList.append(player.team)
        
    return teamList
    

#run program
if __name__ == "__main__":

    #get player lists
    file_path = 'players.csv'
    players = read_csv(file_path)

    #init lineup containers
    initPlayerContainers(list=players)

    teams = initTeamList(list=players)
    
    
    # Variable constraint
    max_budget = 60000
    max_players_from_any_team = 4
    num_lineups = 150
    unique_players = 1

    lineups = []
    for lineup_num in range(num_lineups):
        # Create a linear programming problem
        prob = LpProblem(f"DFS_Lineup_Optimization_{lineup_num + 1}", LpMaximize)
        
        # Define decision variables
        player_vars = LpVariable.dicts("Players", ((player, slot) for slot,mPlayers in lineupSlots.items() for player in mPlayers), 0, 1, LpBinary)

        # Objective function (maximize total projected points)
        prob += lpSum([player.projection * player_vars[player,slot] for slot,mPlayers in lineupSlots.items() for player in mPlayers]), "TotalProjectedPoints"

        # Budget constraint
        prob += lpSum([player.salary * player_vars[player,slot] for slot,mPlayers in lineupSlots.items() for player in mPlayers]) <= max_budget, "BudgetConstraint"

        #Team constraint
        for team in set(teams):
            prob += lpSum([player_vars[player,slot] for slot,mPlayers in lineupSlots.items() for player in mPlayers if player.team == team]) <= max_players_from_any_team, f"AtMost{max_players_from_any_team}PlayersFrom{team}Constraint"
        
        #Choose one player for each slot
        for slot, options in lineupSlots.items():
            prob += lpSum([player_vars[player, slot]  for player in options]) == 1, f"ChooseOnePlayerFor{slot}Constraint"

        #Ensure unique player per position
        for player in set(player for mPlayers in lineupSlots.values() for player in mPlayers):
            prob += lpSum([player_vars[player, pos] for pos, mPlayers2 in lineupSlots.items() if player in mPlayers2]) <= 1, f"UniquePlayer_{player}"
        
        if lineup_num > 0:
            for lineup in lineups:
                #prev_lineup_players = [player for pos, mPlayers in lineupSlots.items() for player in mPlayers if player_vars[player, pos].value() == 1]
                prob += lpSum([player_vars[player, pos] for pos, mPlayers in lineupSlots.items() for player in mPlayers if player not in lineup]) >= unique_players, f"AtLeastOneUniquePlayerInLineup_{lineup_num}_{lineup}"
            
            # prev_lineup_players = [player for pos, mPlayers in lineupSlots.items() for player in mPlayers if player_vars[player, pos].value() == 1]
            # prob += lpSum([player_vars[player, pos] for pos, mPlayers in lineupSlots.items() if player not in prev_lineup_players for player in mPlayers]) >= 1, f"AtLeastOneUniquePlayerInLineup_{lineup_num}"

        # Add the problem to the list of lineups
        prob.solve(PULP_CBC_CMD(msg=0))

        # Print the results for each lineup
        lineup = []
        print("Status:", prob.status)
        print(f"\nOptimal Lineup {lineup_num + 1}:")
        totalPoints = 0
        totalSalary = 0
        totalCount = 0
        for slot, mPlayers in lineupSlots.items():
            for player in mPlayers:
                if player_vars[player,slot].value() == 1:
                    print(f"{player.name} - {player.position}")
                    totalPoints = totalPoints + player.projection
                    totalSalary = totalSalary + player.salary
                    totalCount = totalCount + 1
                    lineup.append(player)

        print("Total Projection: ", totalPoints, " Total Salary:  $", totalSalary, " Count: ", totalCount)
        lineups.append(lineup)
