from pulp import *

#Initialize Problem
lp = LpProblem("Bakery_Problem", LpMaximize)

#Define Variables
x1 = LpVariable(name="Log",lowBound=0, cat="Integer")
x2 = LpVariable(name="Cake",lowBound=0, cat="Integer")

#Objective Function
lp += 10 * x1 + 5 * x2

#Add Constraints
lp += 5 * x1 + x2 <= 90
lp += x1 + 10 * x2 <= 300
lp += 4 * x1  + 6 * x2 <= 125

#Solve
status = lp.solve(PULP_CBC_CMD(msg=0))
print("Status:", status) 

for var in lp.variables():
    print(var, "=", value(var))

print("OPT =", value(lp.objective))
