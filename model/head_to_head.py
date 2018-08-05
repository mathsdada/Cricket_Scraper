class HeadToHead:
    def __init__(self, batsman, bowler, balls=0, runs=0, wickets=0):
        self.batsman = batsman
        self.bowler = bowler
        self.balls = balls
        self.runs = runs
        self.wickets = wickets

    def add_score(self, balls, runs, wicket):
        self.wickets += wicket
        self.balls += balls
        self.runs += runs