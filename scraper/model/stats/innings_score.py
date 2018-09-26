class InningsScore:
    def __init__(self, number, batting_team, bowling_team,
                 runs_scored, wickets_lost, overs_played):
        self.__number = number
        self.__batting_team = batting_team
        self.__bowling_team = bowling_team
        self.__runs = runs_scored
        self.__wickets = wickets_lost
        self.__overs = overs_played

        self.__batting_scores = []
        self.__bowling_scores = []

    def get_innings_number(self):
        return self.__number

    def get_batting_team_name(self):
        return self.__batting_team

    def get_bowling_team_name(self):
        return self.__bowling_team

    def get_runs(self):
        return self.__runs

    def get_wickets(self):
        return self.__wickets

    def get_overs(self):
        return self.__overs

    def set_batting_scores(self, batting_scores):
        self.__batting_scores = batting_scores

    def get_batting_scores(self):
        return self.__batting_scores

    def set_bowling_scores(self, bowling_scores):
        self.__bowling_scores = bowling_scores

    def get_bowling_scores(self):
        return self.__bowling_scores
