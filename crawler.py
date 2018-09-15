from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
import csv
import ComputeRating as cr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



standings_url = "https://play.esea.net/index.php?s=league&d=standings&division_id=3121"
base_url = "https://play.esea.net"
team_urls = []
team_names = []
team_stats_list = []  # Team Name, Home, Away, Map, Result, Score, Date
team_stats = ['', '',  '',  '', '', '', '']

big_data = []
path = r"D:/School/Python/Rating/chromedriver.exe"


# Open up a chrome browser and get IM Standings page
driver = webdriver.Chrome()
driver.get(standings_url)

element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "league-standings")))
print("Ready")

league_standings = soup(driver.page_source, 'html.parser')
table_rows = league_standings.find("table").find(
    'tbody').find_all("tr", {"class": ["row1", "row2"]})

for i in range(0, len(table_rows)):
    cells = table_rows[i].find_all("td")
    anchors = cells[0].find_all("a")
    team_names.append(anchors[len(anchors) - 1].text)
    team_urls.append(base_url + str(anchors[len(anchors) - 1]['href']))

for i in range(0, len(table_rows)):
    url_team = team_urls[i]
    driver.get(team_urls[i])
    team_page = soup(driver.page_source, 'html.parser')
    match_list = team_page.find("table").find('tbody').find_all("tr")
    for row in match_list:
        cells = row.find_all('td')
        if(len(cells) == 7):
            if(cells[4].find('a') is None):
                break
            else:
                team_stats[0] = team_names[i]
                team_stats[1] = cells[1].find('a').text
                team_stats[2] = cells[2].find('a').text
                team_stats[3] = cells[3].text
                team_stats[4] = cells[4].find('a').text
                team_stats[5] = cells[5].find('a').text
                team_stats[6] = cells[6].find('a').text
                team_stats_list.append(team_stats)
                with open(r'stats', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(team_stats)
    time.sleep(4.2)

with open('stats.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    team_stats_list = list(reader)

length = len(team_stats_list)

for i in range(0, len(team_stats_list)):
    if(i % 2 == 0):
        big_data.append(team_stats_list[i])
    else:
        pass

with open('big_data.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(big_data)

cr.CalculateRating()
