class HeadToHead:
    def __init__(self, batsman, bowler, balls=0, runs=0, wickets=0):
        self.__batsman = batsman
        self.__bowler = bowler
        self.__balls = balls
        self.__runs = runs
        self.__wickets = wickets
        self.__dot_balls = 0

    def add_score(self, balls, runs, wicket):
        self.__wickets += wicket
        self.__balls += balls
        self.__runs += runs

    def get_batsman(self):
        return self.__batsman

    def get_bowler(self):
        return self.__bowler

    def get_balls(self):
        return self.__balls

    def get_runs(self):
        return self.__runs

    def get_wickets(self):
        return self.__wickets

    def get_dot_balls(self):
        return self.__dot_balls
