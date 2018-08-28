class Series:
    def __init__(self, title):
        self.title = title
        self.format = []
        self.matches_list = []

    def add_format(self, format):
        self.format = format

    def add_match(self, match):
        self.matches_list.append(match)
