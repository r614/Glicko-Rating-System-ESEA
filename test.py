# Test code
import csv
with open('stats', 'r', newline='') as f:
    reader = csv.reader(f)
    team_stats_list = list(reader)
    print(team_stats_list)

length = len(team_stats_list)

stats_list_filtered = []
r = 0
length = len(team_stats_list)
while r < length:
    search = team_stats_list[r]
    if (search[0] == 'Animus Gaming'and search[-1] == 'Jul 9 18'):
        stats_list_filtered.append(search[:])
        r = length
        print(stats_list_filtered)
    else:
        for i in range(0, len(stats_list_filtered)):
            if(search[1:] == stats_list_filtered[i][1:]):
                pass
            else:
                stats_list_filtered.append(search[:])
                print(stats_list_filtered)
                r = r + 1
                break
with open('stats_filtered', 'w', newline=',') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(stats_list_filtered)
