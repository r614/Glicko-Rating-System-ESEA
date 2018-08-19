# Test code
import csv

match_list = []
duplicate_list = []

class Match:
    def __init__(self, teams, map, date):
        self.teams = []
        for team in teams:
            self.teams.append(team)
        self.teams = sorted(self.teams)
        self.map = map
        self.date = date
    def __eq__(self, other):
        return self.__dict__ == other.__dict__



'''with open('stats', 'r') as f, open('no_rows.csv', 'w', newline = '') as output:
    reader = csv.reader(f)
    output_file = csv.writer(output)
    index = 0
    for row in reader:
        if(index%2 == 0):
            output_file.writerow(row)
        index+=1
'''
with open('no_rows.csv', 'r') as input:
    reader = csv.reader(input)
    index = 0
    for row in reader:
        team_list = []
        team_list.append(row[1])
        team_list.append(row[2])
        match = Match(team_list, row[3], row[6])
        if match in match_list:
            duplicate_list.append(match)
            print(index, match_list.index(match), match_list[match_list.index(match)].teams)
            print(match.teams)
        else:
            match_list.append(match)
        index += 1
#for match in match_list:
 #   print(match.teams, match)
print(len(match_list))
print(len(duplicate_list))

'''length = len(team_stats_list)
print(length)
print(team_stats_list[0])


stats_list_filtered = ['', '',  '',  '', '', '', '']
for r in range(0, length):
    print(r)
    search = team_stats_list[r]
    for i in range(0, len(stats_list_filtered)):
        if(search[1:] == stats_list_filtered[i][1:]):
            pass
        else:
            stats_list_filtered.append(search)'''

with open('Book1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for match in match_list:
        writer.writerow([match.teams, match.date, match.map])
