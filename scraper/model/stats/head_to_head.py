class HeadToHead:
    def __init__(self, batsman, batsman_team, bowler, bowler_team):
        self.__batsman = batsman
        self.__batsman_team = batsman_team
        self.__bowler = bowler
        self.__bowler_team = bowler_team
        self.__balls = 0
        self.__runs = 0
        self.__wickets = 0
        self.__dot_balls = 0
        self.__fours = 0
        self.__sixes = 0

    def add_score(self, balls, runs, wicket):
        self.__wickets += wicket
        self.__balls += balls
        self.__runs += runs
        if (balls == 1) and (runs == 0):
            self.__dot_balls += 1
        if runs == 4:
            self.__fours += 1
        if runs == 6:
            self.__sixes += 1

    def get_batsman(self):
        return self.__batsman

    def get_batsman_team(self):
        return self.__batsman_team

    def get_bowler(self):
        return self.__bowler

    def get_bowler_team(self):
        return self.__bowler_team

    def get_balls(self):
        return self.__balls

    def get_runs(self):
        return self.__runs

    def get_wickets(self):
        return self.__wickets

    def get_dot_balls(self):
        return self.__dot_balls

    def get_num_fours(self):
        return self.__fours

    def get_num_sixes(self):
        return self.__sixes
