class Venue:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def match_scores(self, venue, format, num_of_matches):
        pass

    def best_batsmen(self, venue, format, num_of_matches):
        pass

    def best_bowlers(self, venue, bowler_names, format, num_of_matches):
        pass

    def wickets_per_bowling_style(self, venue, bowling_style, format, num_of_matches):
        pass

    def per_innings_avg_score(self, venue, format, num_of_matches):
        pass

    def team_batting_first_win_count(self, venue, format, number_of_matches):
        pass

    def team_batting_second_win_count(self, venue, format, number_of_matches):
        pass
