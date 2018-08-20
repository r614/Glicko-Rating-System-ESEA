import csv


class Match:
    def __init__(self, home, away, map, result, score, date):
        self.home = home
        self.away = away
        self.map = map
        self.date = date
        self.result = result
        self.score = score

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

    def stat_row(self):
        return '{}  {}  {}  {}  {}  {}'.format(self.home, self.away, self.map, self.result, self.score, self.date)


standings_url = "https://play.esea.net/index.php?s=league&d=standings&division_id=3121"
base_url = "https://play.esea.net"
team_urls = []
team_names = []
team_scores_and_names_dict = {}
team_stats_list = []  # Team Name, Home, Away, Map, Result, Score, Date
team_stats = ['', '',  '',  '', '', '', '']
stats_list_filtered = []
big_data = []
duplicate_list = []
match_list = []
path = r"D:/School/Python/Rating/chromedriver.exe"

with open('stats', 'r', newline='') as f:
    reader = csv.reader(f)
    team_stats_list = list(reader)

length = len(team_stats_list)

for i in range(0, len(team_stats_list)):
    if(i % 2 == 0):
        big_data.append(team_stats_list[i])
    else:
        pass

index = 0
for row in big_data:
    match = Match(row[1], row[2], row[3], row[4], row[5], row[6])
    if match in match_list:
        duplicate_list.append(match)
    else:
        match_list.append(match)
    index += 1

with open('Book2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for match in match_list:
        writer.writerow([match.stat_row()])
