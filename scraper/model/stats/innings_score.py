class InningsScore:
    def __init__(self, number, batting_team, bowling_team,
                 runs_scored, wickets_lost, overs_played):
        self.number = number
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.runs_scored = runs_scored
        self.wickets_lost = wickets_lost
        self.overs_played = overs_played
        self.batting_scores = []
        self.bowling_scores = []

    def set_batting_scores(self, batting_scores):
        self.batting_scores = batting_scores

    def get_batting_scores(self):
        return self.batting_scores

    def set_bowling_scores(self, bowling_scores):
        self.bowling_scores = bowling_scores

    def get_bowling_scores(self):
        return self.bowling_scores
