class BatsmanScore:
    def __init__(self, player_name, runs_scored, balls_played, num_fours, num_sixes):
        self.__name = player_name
        self.__runs = runs_scored
        self.__balls = balls_played
        self.__fours = num_fours
        self.__sixes = num_sixes

    def get_name(self):
        return self.__name

    def get_runs(self):
        return self.__runs

    def get_balls(self):
        return self.__balls

    def get_fours(self):
        return self.__fours

    def get_sixes(self):
        return self.__sixes
