class BowlerScore:
    def __init__(self, player_name, overs_bowled, wickets_taken, runs_given, economy):
        self.__name = player_name
        self.__overs = overs_bowled
        self.__wickets = wickets_taken
        self.__runs = runs_given
        self.__economy = economy

    def get_name(self):
        return self.__name

    def get_overs(self):
        return self.__overs

    def get_wickets(self):
        return self.__wickets

    def get_runs(self):
        return self.__runs

    def get_economy(self):
        return self.__economy
