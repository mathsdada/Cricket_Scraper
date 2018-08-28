class Match:
    def __init__(self, title, format, teams, date, venue):
        self.title = title
        self.format = format
        # teams is a dictionary in below form
        # {'team-1' : [team-1's squad], 'team-2' : [team-2's squad]}
        self.teams = teams
        self.date = date
        self.venue = venue
