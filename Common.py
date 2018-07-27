class Player:
    def __init__(self, name="", player_id="", role="", bat_style="", bowl_style=""):
        self.name = name
        self.player_id = player_id
        self.role = role
        self.bat_style = bat_style
        self.bowl_style = bowl_style


class Batsman:
    def __init__(self, player=None, runs_scored=0, balls_played=0, status="TBD"):
        self.player = player
        self.runs_scored = runs_scored
        self.balls_played = balls_played
        self.status = status


class Bowler:
    def __init__(self, player=None, balls_bowled=0, wickets_taken=0, runs_given=0):
        self.player = player
        self.balls_bowled = balls_bowled
        self.wickets_taken = wickets_taken
        self.runs_given = runs_given


class InningsScore:
    def __init__(self, number, team,
                 runs_scored, wickets_lost, overs_played,
                 batsmen_score=None, bowlers_score=None):
        if batsmen_score is None:
            batsmen_score = []
        if bowlers_score is None:
            bowlers_score = []
        self.number = number
        self.team = team
        self.runs_scored = runs_scored
        self.wickets_lost = wickets_lost
        self.overs_played = overs_played
        self.batsmen_score = batsmen_score
        self.bowlers_score = bowlers_score


class Match:
    def __init__(self, title="", date="",
                 format="", teams=None, venue="", result="", scores=None):
        # scores is a list of InningsScore
        # teams is a list of playing team names
        if scores is None:
            scores = []
        if teams is None:
            teams = []
        self.title = title
        self.date = date
        self.format = format
        self.teams = teams
        self.venue = venue
        self.result = result
        self.scores = scores
