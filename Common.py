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


class HeadToHead:
    def __init__(self, batsman, bowler, balls=0, runs=0, wicket=False):
        self.batsman = batsman
        self.bowler = bowler
        self.balls = balls
        self.runs = runs
        self.wicket = wicket

    def add_score_per_ball(self, runs, wicket):
        if not self.wicket:
            self.wicket = wicket
            self.balls += 1
            self.runs += runs
        else:
            raise Exception("Entering HeadToHead even after batsman is out...Have you gone mad..check it bitch!!!!!")

    def add_score(self, balls, runs, wicket):
        if (not self.wicket) and (balls != 0):
            self.wicket = wicket
            self.balls += balls
            self.runs += runs
        else:
            raise Exception("Something Wrong with the input. (balls={}, runs={}, wicket={})"
                            .format(balls, runs, wicket))


class Match:
    def __init__(self, title="", date="",
                 format="", teams=None, venue="", result="", scores=None, head_to_head=None):
        if scores is None:
            # scores is a list of InningsScore
            scores = []
        if teams is None:
            # teams is a list of playing team names
            teams = []
        if head_to_head is None:
            # head_to_head is list of HeadToHead class instances
            head_to_head = []
        self.title = title
        self.date = date
        self.format = format
        self.teams = teams
        self.venue = venue
        self.result = result
        self.scores = scores
        self.head_to_head = head_to_head
