class Team:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def team_form(self, team_name, format, num_of_matches):
        # Win - Loss like (W L L W W W L L). Get opposite team name as well.
        pass

    def team_match_scores(self, team_name, format, num_of_matches):
        pass

    def most_runs(self, team_squad, format, num_of_matches):
        # batsman_name num_matches runs balls highest_score
        # Array of above
        pass

    def most_wickets(self, team_squad, format, num_of_matches):
        # bowler_name num_matches wickets runs
        # Array of above
        pass

    def best_economy(self, team_squad, format, num_of_matches):
        # bowler_name num_matches overs runs wickets economy
        # Array of above
        pass

    def record_against_opposite_team(self, team_name, opposite_team_name, format, num_of_matches):
        pass

    def team_form_at_venue(self, team_name, venue, format, num_of_matches):
        pass

    def team_match_scores_at_venue(self, team_name, venue, format, num_of_matches):
        pass

    def most_runs_at_venue(self, team_squad, venue, format, num_of_matches):
        # batsman_name num_matches runs balls highest_score
        # Array of above
        pass

    def most_wickets_at_venue(self, team_squad, venue, format, num_of_matches):
        # bowler_name num_matches wickets runs
        # Array of above
        pass

    def best_economy_at_venue(self, team_squad, venue, format, num_of_matches):
        # bowler_name num_matches overs runs wickets economy
        # Array of above
        pass

    def record_against_opposite_team_at_venue(self, team_name, opposite_team_name, venue, format, num_of_matches):
        pass
