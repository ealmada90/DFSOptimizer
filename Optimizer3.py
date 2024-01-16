import csv
from DFSPlayer import *
from pulp import *

#declare variables
lineupSlots = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
positionRequirements = ["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"]

#declare functions
def create_player_from_row(row):

    return DFSPlayer(int(row['\ufeffLineStarId']), row['Name'], row['Team'], row['Position'], int(row['Salary']), float(row['Projected']))

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
    initPlayerContainers(list=players)

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
        
        # Define decision variables (binary variables indicating whether a player is selected for each lineup slot)
        lineup_slots = { (slot): LpVariable(name=f"{slot}", cat='Binary') for slot,slotPlayers in lineupSlots.items()}


        # Objective function: Maximize total projected points
        prob += lpSum(lineup_slots[slot] * players[playerId].projection for slot in lineup_slots for playerId in lineupSlots[slot])



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
                print(f"{players[playerId].name} - {players[playerId].position}")
                totalPoints = totalPoints + players[playerId].projection
                totalSalary = totalSalary + players[playerId].salary
                totalCount = totalCount + 1
                lineup.append(playerId)
                players[playerId].ownership += 1

        print("Total Projection: ", totalPoints, " Total Salary:  $", totalSalary, " Count: ", totalCount, "\n")
        lineups.append(lineup)
    


