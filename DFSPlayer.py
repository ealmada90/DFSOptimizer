class DFSPlayer:
    def __init__(self, id,  name, team, positions, salary, projection):
        self.name = name
        self.team = team
        self.positions = positions
        self.salary = salary
        self.projection = projection
        self.id = id
        self.ownership = 0

    def __str__(self):
        return f"{self.name} {self.projection}"

    def myfunc(self):
        print("Hello my name is " + self.name)