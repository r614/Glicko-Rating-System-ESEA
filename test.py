import csv


class Match:
    def __init__(self, teams, map, result, score, date):
        self.teams = []
        for team in teams:
            self.teams.append(team)
        self.teams = sorted(self.teams)
        self.map = map
        self.date = date
        self.result = result
        self.score = score

        def __eq__(self, other):
            return self.__dict__ == other.__dict__


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
    team_list = []
    team_list.append(row[1])
    team_list.append(row[2])
    match = Match(team_list, row[3], row[4], row[5], row[6])
    if match in match_list:
        duplicate_list.append(match)
        print(index, match_list.index(match), match_list[match_list.index(match)].teams)
        print(match.teams)
    else:
        match_list.append(match)
    index += 1

with open('Book1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for match in match_list:
        writer.writerow([match.teams, match.map, match.result, match.score, match.date])
