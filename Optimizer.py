import csv
from Objects.DFSPlayer import *
from Objects.OptimizerSettings import *
from pulp import *
import json


#declare variables
lineupSlots = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
positionRequirements = ["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"]

#declare functions
def create_player_from_row(row):
    positions = row['Position'].split("/")
    return DFSPlayer(int(row['\ufeffLineStarId']), row['Name'], row['Team'], positions, int(row['Salary']), float(row['Projected']))

def initPlayersDictionary(list):
    players = {}
    for p in list:
        s = json.dumps(p)
        j = json.loads(s)
        player = DFSPlayer(**j)
        if(player.projection > 0):
            player.positions = player.positions.split("/")
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
    
ordered_positions = ['PG', 'PG', 'SG', 'SG', 'SF', 'SF', 'PF', 'PF', 'C']
def orderLineup(lineup, dictionary):
    orderedLineup = []
    for index in range(9):
        for playerId in lineup:
            if(dictionary[playerId] == ordered_positions[index] and playerId not in orderedLineup):
                orderedLineup.append(playerId)

                break

    return orderedLineup

def initOptimizerSettings(settings):
        s = json.dumps(settings)
        j = json.loads(s)
        settings = OptimizerSettings(**j)
        return settings

#run program
def optimizerLineups(playerList, optimizer_settings):

   
    players = initPlayersDictionary(playerList)
    settings = initOptimizerSettings(settings=optimizer_settings)
    teams = initTeamList(list=players)
    

    
    # Variable constraint
    max_budget = settings.budget
    max_players_from_any_team = settings.max_players_per_team
    num_lineups = settings.num_lineups
    unique_players = settings.unique_players
    Global_Ownership = settings.max_exposure / 100

   

    print("\n")
    print(f"Optimizing {settings.num_lineups} lineups")
    print(f"Pool size: {len(players.keys())}")
    print(f"Max Budget: {settings.budget}")
    print(f"Min Budget: {settings.min_budget}")
    print(f"Max per Team: {settings.max_players_per_team}")
    print(f"Max Exposure: {settings.max_exposure}")
    print(f"Max Budget: {settings.unique_players}")

    print("\nStarting Optimization")
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
        positionDictionary = {}
        lineup = []
        print(f"Optimized Lineup {lineup_num + 1}:")       
        for playerId in player_vars:
            for position in players[playerId].positions:
                if position_vars[playerId, position].value() == 1:
                    lineup.append(playerId)
                    positionDictionary[playerId] = position
                    players[playerId].ownership += 1

        
        
        orderedLineup = orderLineup(lineup=lineup,dictionary=positionDictionary)
        lineups.append(orderedLineup)


    return lineups
