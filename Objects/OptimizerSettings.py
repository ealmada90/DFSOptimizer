class OptimizerSettings:
    def __init__(self, site, sport, num_lineups, budget, min_budget, unique_players, max_exposure, stack_count, stack_size, max_players_per_team):
        self.site = site
        self.sport = sport
        self.num_lineups = num_lineups
        self.budget = budget
        self.min_budget = min_budget
        self.unique_players = unique_players
        self.max_exposure = max_exposure
        self.stack_count = stack_count
        self.stack_size = stack_size
        self.max_players_per_team = max_players_per_team

    def __str__(self):
        return f"{self.site} {self.sport} {self.num_lineups} {self.budget}"

    def myfunc(self):
        print("Hello my name is " + self.name)