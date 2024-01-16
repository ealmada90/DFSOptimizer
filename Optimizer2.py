import csv
from DFSPlayer import *
from pulp import *

#declare variables
lineupSlots = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
positionRequirements = ["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"]

#declare functions
def create_player_from_row(row):
    positions = row['Position'].split("/")
    return DFSPlayer(int(row['\ufeffLineStarId']), row['Name'], row['Team'], positions, int(row['Salary']), float(row['Projected']))

def read_csv(file_path):
    players = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = create_player_from_row(row=row)
            if(player.projection > 0):
                players[player.id] = player
    return players

def initPlayerNames(list):
    returnList = []
    for player in list:
        if player.name not in returnList:
            returnList.append(player.name)
    return returnList

def initPlayerContainers(list):
    for slot,players in lineupSlots.items():
        for playerId in list:
            if(positionRequirements[slot] in list[playerId].position):
                players.append(playerId)

def initPlayerList(list):
    returnList = []
    for player in list:
        if("/" in player.position):
            positions = player.position.split("/")
            for pos in positions:
                p = DFSPlayer(player.name, player.team, pos, player.salary, player.projection)
                returnList.append(p)
        else:
            returnList.append(player)

    return returnList

def initTeamList(list):
    teamList = []
    for playerId in list:
        if(list[playerId].team not in teamList):
            teamList.append(list[playerId].team)
        
    return teamList
    

#run program
if __name__ == "__main__":

    #get player lists
    file_path = 'players.csv'
    players = read_csv(file_path)
    ###names = initPlayerNames(list = players)
    ###players = initPlayerList(list=players)
    #init lineup containers
    ##initPlayerContainers(list=players)

    teams = initTeamList(list=players)
    
    
    # Variable constraint
    max_budget = 60000
    max_players_from_any_team = 4
    num_lineups = 20
    unique_players = 1
    Global_Ownership = 0.5

    print("\n")
    lineups = []
    for lineup_num in range(num_lineups):
        # Create a linear programming problem
        prob = LpProblem(f"DFS_Lineup_Optimization_{lineup_num + 1}", LpMaximize)
        
        # Define decision variables
        player_vars = {(playerId): LpVariable(name=f"{playerId}", cat='Binary') for playerId in players.keys()}
        position_vars = {(playerId, position): LpVariable(name=f"{playerId}_{position}_var", cat='Binary') for playerId in players.keys() for position in players[playerId].positions}


        # Objective function (maximize total projected points)
        prob += lpSum([players[playerId].projection * player_vars[playerId] for playerId in player_vars])

        # Budget constraint
        prob += lpSum([players[playerId].salary * player_vars[playerId] for playerId in player_vars]) <= max_budget

        #Team constraint
        for team in set(teams):
            prob += lpSum([player_vars[playerId] for playerId in player_vars if players[playerId].team == team]) <= max_players_from_any_team

        # position Constraint
        position_limits = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 2, 'C': 1}
        for position, limit in position_limits.items():
            prob += lpSum(position_vars.get((playerId, position), 0) for playerId in players.keys()) == limit

        # Constraint 3: Each player is assigned to at most one position
        for playerId in players.keys():
            prob += lpSum(position_vars.get((playerId, position), 0) for position in players[playerId].positions) <= 1

        # Constraint 4: Link player and position variables
        for playerId in players.keys():
            for position in players[playerId].positions:
                prob += position_vars[(playerId, position)] <= player_vars[playerId]

        if lineup_num > 0:
            for playerId in players.keys():
                prob += (1 + players[playerId].ownership) * player_vars[playerId] <= Global_Ownership * num_lineups

            for lineup in lineups:
                #prev_lineup_players = [player for pos, mPlayers in lineupSlots.items() for player in mPlayers if player_vars[player, pos].value() == 1]
                prob += lpSum([player_vars[playerId] for playerId in player_vars if playerId not in lineup]) >= unique_players

        # Solve problem
        prob.solve(PULP_CBC_CMD(msg=0))

        # Print the results for each lineup
        lineup = []
        print("Status:", prob.status)
        print(f"Optimal Lineup {lineup_num + 1}:")
        totalPoints = 0
        totalSalary = 0
        totalCount = 0
        for playerId in player_vars:
            if player_vars[playerId].value() == 1:
                print(f"{players[playerId].name} - {players[playerId].positions}")
                totalPoints = totalPoints + players[playerId].projection
                totalSalary = totalSalary + players[playerId].salary
                totalCount = totalCount + 1
                lineup.append(playerId)
                players[playerId].ownership += 1

        print("Total Projection: ", totalPoints, " Total Salary:  $", totalSalary, " Count: ", totalCount, "\n")
        lineups.append(lineup)
    
    print("Ownership report")
    for playerId,player in players.items():
        if(player.ownership > 0):
            print(player.name + " - " + f"{float(100 * (player.ownership/num_lineups))}" + "%")


