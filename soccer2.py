
import pandas as pd
import soccerdata as sd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

understat_previous = sd.Understat(leagues="ENG-Premier League", seasons="2025")

schedule_previous = understat_previous.read_schedule()
schedule_previous.head()
schedule_previous = schedule_previous.reset_index(drop=True)
#print(schedule)

teams_last_season_points = dict()
for row in schedule_previous["home_team"]:
    if row not in teams_last_season_points: #teams_last_season_points[row] = teams_last_season_points.get(row,0)    Alternate way of writing line. Add + 1 at end to make something to count all times word was mentioned.
        teams_last_season_points[row] = 0
#print(teams_last_season)

for i, row in schedule_previous.iterrows(): #Counting how many points each team had in the previous season. With two iteration variables! One looks at the index label (0,1,2,..) and the other looks at the the entire row's data
    home = row["home_team"]                 # read by column name in this case. iterrows() Iterate over DataFrame rows as (index, Series) pairs.
    away = row["away_team"]
    if row["home_goals"] > row["away_goals"]:
        teams_last_season_points[home] += 3 # x += 1 is shorthand for x = x+1
    elif row["home_goals"] < row["away_goals"]:
        teams_last_season_points[away] += 3
    else:
        teams_last_season_points[away] += 1
        teams_last_season_points[home] += 1
#print(teams_last_season_points)

last_season_standings = list()
for key, val in teams_last_season_points.items(): #.items() unpacks the keys and values into seperate variables. 
    tup1 = (val, key)
    last_season_standings.append(tup1) #Making a list of tuples in value/key pairs,
last_season_standings = sorted(last_season_standings, reverse = True) # then sorting them by value from largest to smallest,
#for val, key in last_season_standings:
    #print (val, key) # and finally printing them in order of value/key because print(lst) prints them in a way that is harder to read.

last_season_standings_names = list() # last_season_standings_names = [] says the same thing.
for points, team in last_season_standings: #This makes a list of only team names. I'm keeping this seperate from last_season_standings because I want to find the standard deviation using the points. I may do this with the dict().
    last_season_standings_names.append(team) #Index variables work like []. for [] in [[0,1],[1,2],[2,3]] is the same as saying: look at [:1] for each thing.



