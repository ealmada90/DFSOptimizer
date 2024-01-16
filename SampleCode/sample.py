from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary

# Example data (replace this with your actual data)
players_data = [
    ('Player1', 20, 10, 'TeamA'),
    ('Player2', 18, 12, 'TeamB'),
    ('Player3', 25, 15, 'TeamA'),
    ('Player4', 22, 14, 'TeamC'),
    ('Player5', 15, 8, 'TeamA'),
    ('Player6', 19, 10, 'TeamB'),
    ('Player7', 21, 11, 'TeamC'),
    ('Player8', 16, 9, 'TeamA'),
    ('Player9', 17, 10, 'TeamB'),
]

# Define lineup slots and player options for each slot
lineup_slots = {
    'QB': [
        ('Player1', 20, 10, 'TeamA'),
        ('Player2', 18, 12, 'TeamB'),
        ('Player3', 25, 15, 'TeamA'),
    ],
    'RB': [
        ('Player4', 22, 14, 'TeamC'),
        ('Player5', 15, 8, 'TeamA'),
        ('Player6', 19, 10, 'TeamB'),
    ],
    'WR': [
        ('Player7', 21, 11, 'TeamC'),
        ('Player8', 16, 9, 'TeamA'),
        ('Player9', 17, 10, 'TeamB'),
    ],
}

# Budget constraint
budget = 100

# Create Player instances from the data
class Player:
    def __init__(self, name, projected_points, cost, team):
        self.name = name
        self.projected_points = projected_points
        self.cost = cost
        self.team = team

players = [Player(name, points, cost, team) for name, points, cost, team in players_data]

# Create a linear programming problem
prob = LpProblem("DFS_Lineup_Optimization", LpMaximize)

# Define decision variables
player_vars = LpVariable.dicts("Players", players, 0, 1, LpBinary)

# Objective function (maximize total projected points)
prob += lpSum([player.projected_points * player_vars[player] for player in players]), "TotalProjectedPoints"

# Budget constraint
prob += lpSum([player.cost * player_vars[player] for player in players]) <= budget, "BudgetConstraint"

# Position constraints (choose one player for each lineup slot)
for slot, options in lineup_slots.items():
    prob += lpSum([player_vars[player] for player in players if player in options]) == 1, f"ChooseOnePlayerFor{slot}Constraint"



# Solve the problem
prob.solve()

# Print the results
print("Status:", prob.status)
print("Optimal Lineup:")
for slot in lineup_slots:
    selected_player = next((player for player in players if player_vars[player].value() == 1 and player in lineup_slots[slot]), None)
    if selected_player:
        print(f"{slot}: {selected_player.name} - Projected Points: {selected_player.projected_points}, Cost: {selected_player.cost}, Team: {selected_player.team}")
    else:
        print(f"No valid player selected for {slot}")
