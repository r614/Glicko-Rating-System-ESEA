# Test code
import csv


with open('stats', 'r') as f:
    reader = csv.reader(f)
    team_stats_list = list(reader)
length = len(team_stats_list)

stats_list_filtered = ['', '',  '',  '', '', '', '']
for r in range(0, length):
    search = team_stats_list[r]
    for i in range(0, len(stats_list_filtered)):
        if(search[1:] == stats_list_filtered[i][1:]):
            pass
        else:
            stats_list_filtered.append(search)

with open(r'test_filter.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerows(stats_list_filtered)
