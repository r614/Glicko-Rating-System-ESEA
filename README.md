# Glicko-Rating-System-ESEA
Scrapes ESEA for leaderboard data and rates teams using Glicko-2 Rating System

1. Download or clone the repository.
2. Change path in line 20 of crawler.py such that it points to the location of chromedriver.exe on your computer. 
3. Run crawler.py. I recommend leaving it overnight as it does take a lot of time to scrape data from the website.
4. The file will save scraped data as stats.csv and big_data.csv while the ratings will be saved in finalrating.csv


Notes: 

If you have existing scraped data and wish to compute ratings, you can save your csv file as big_data.csv in the same folder as ComputeRating.py and run the script. 

I would not recommend changing the sleep values at the risk of getting rate limited and facing a temporary ban from ESEA.

The code can be easily adapted to rate other games - though by the default the match input format is: team_name, home, away, map, result, score, date.
