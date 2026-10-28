import pandas as pd
import soccerdata as sd
import sys

pd.set_option("display.max_columns", None) #no column limit
pd.set_option("display.width", None) #don't wrap columns onto new lines

understat = sd.Understat(leagues="ENG-Premier League", seasons="2026")
understat_previous = sd.Understat(leagues="ENG-Premier League", seasons="2025")

shot_events = understat.read_shot_events()
shot_events.head() #shot events - when shot was taken, situation (ex. open play, free kick, etc.), result (shot blocked, missed, scored, etc.)
shot_events = shot_events.reset_index(drop=True)
#print(shot_events)

schedule = understat.read_schedule() 
schedule.head() #game schedule inluding final scores
schedule = schedule.reset_index(drop=True) #turning index levels into regular columns to avoid 'KeyError'. The top row of labels are now a regular column.
#print(schedule)

schedule_previous = understat_previous.read_schedule()
schedule_previous.head()
schedule_previous = schedule_previous.reset_index(drop=True)
#print(schedule)


games_played = schedule[schedule['is_result'].fillna(False)] #flitering datatable by games that have been played (table inlcude games scheduled for future) and (as a precaution) set values that are neither true/false (nan) to false.

matches_played = dict() #The begining of counting how many total games have been played.
for i, row in games_played.iterrows():
    for team in (row["home_team"], row["away_team"]):
        if team not in matches_played:
            matches_played[team] = 1
        else:
            matches_played[team] +=1
print(matches_played)



sys.exit()

recent_games = games_played.iloc[-10:] #The syntax of .iloc in Pandas is: df.iloc[row_indexer, column_indexer]. ***Want to order games by week, or games played***
recent_games = recent_games.reset_index(drop=True)
#print(recent_games[['date','home_team','away_team']],'\n') #,'home_goals','away_goals' #use [[]] to access multiple columns.



teams_last_season_points = dict()
for row in schedule_previous["home_team"]:
    if row not in teams_last_season_points: #teams_last_season_points[row] = teams_last_season_points.get(row,0)    Alternate way of writing line. Add  + 1 at end to make something to count all times word was mentioned.
        teams_last_season_points[row] = 0
#print(teams_last_season)

for i, row in schedule_previous.iterrows(): #counting how many points each team had in the previous season. With two iteration variables! One looks at the index label (0,1,2,..) and the other looks at the the entire row's data
    home = row["home_team"]                 # read by column name in this case.
    away = row["away_team"]
    if row["home_goals"] > row["away_goals"]:
        teams_last_season_points[home] += 3
    elif row["home_goals"] < row["away_goals"]:
        teams_last_season_points[away] += 3
    else:
        teams_last_season_points[away] += 1
        teams_last_season_points[home] += 1

last_season_standings = list()
for key, val in teams_last_season_points.items(): #.items() unpacks the keys and values into seperate variables.
    tup1 = (val, key)
    last_season_standings.append(tup1) #making a list of tuples in value/key pairs,
last_season_standings = sorted(last_season_standings, reverse = True) # then sorting them by value from largest to smallest,

#for val, key in last_season_standings:
    #print (val, key) # and finally printing them in order of value/key because print(lst) prints them in a way that is harder to read.
#print('\n')


teams_this_season = [] #Need two lists of only team names from this and last season to make list of newly promoted teams.
for row in schedule['home_team']:
    if row not in teams_this_season: #last_season_standings and not
        teams_this_season.append(row)

teams_last_season = []
for row in schedule_previous['home_team']:
    if row not in teams_last_season:
        teams_last_season.append(row) 

top90th = last_season_standings[:2] #2  Later may break this into percentiles as opposed to final standings. Might be worth averaging the last 2 seasons standings as well.
top75th = last_season_standings[2:5] #3
top50th = last_season_standings[5:10] #5
top25th = last_season_standings[10:15] #5
top0th = last_season_standings[15:17] #2

newlypromo = [] #3
for team in teams_this_season:
    if team not in teams_last_season:
        newlypromo.append(team)

bot5 = top0th + newlypromo
top5 = top75th + top90th
bothalf = top25th + top0th + newlypromo
tophalf = top50th + top75th + top90th

yindx = -1
for i in range(len(recent_games)): #range(10)
    yindx = yindx+1
    
    homeg = recent_games.loc[yindx,'home_goals']
    awayg = recent_games.loc[yindx,'away_goals']

    homet = recent_games.loc[yindx,'home_team']
    awayt = recent_games.loc[yindx,'away_team']

    print(recent_games.loc[yindx,'home_team']) #,homeg
    print(recent_games.loc[yindx,'away_team']) #,awayg
    print(recent_games.loc[yindx,'date'])

    hg=float(homeg)
    ag=float(awayg)
    if hg > ag:
         winningt = recent_games.loc[yindx,'home_team']
         losingt = recent_games.loc[yindx,'away_team']
    elif hg < ag:
        winningt = recent_games.loc[yindx,'away_team']
        losingt = recent_games.loc[yindx,'home_team']
    else:
        winningt = 'tie'
        losingt = 'tie'
    
    gamescore=0
    if hg+ag >=4 and abs(hg-ag) <= 1: #were there 4 or more goals scored where the final scoreline was within 1 goal.
        gamescore += 2
    if hg+ag >=6 and abs(hg-ag) <= 2: #were there 6 or more goals scored where the final scoreline was within 2 goals.
        gamescore += 2
    if abs(hg-ag) !=0 and hg+ag > 1: #was the difference in the scoreline not 0, did the game not tie. Was there a winner. AND was there more than 1 goal scored in the match.
        gamescore += 1
    if hg+ag > 0: #were there any goals scored.
        gamescore += 1
    
    if winningt in bot5 and losingt in tophalf:
        gamescore += 1
    if winningt in bot5 and losingt in top5:
        gamescore += 1
    if winningt in bot5 and losingt in top90th: # +5 points for a team in bot5 if they beat the top 2 teams last season.
        gamescore += 2
    if ((homet, awayt) in bot5 and winningt == 'tie') and ((homet, awayt) in top5):
        gamescore += 1
    if ((homet, awayt) in newlypromo and winningt == 'tie') and ((homet, awayt) in top90th):
        gamescore += 1
    '''
    if (winningt in top_0th or top25th) and losingt in top75th:
        gamescore += 2
    if (winningt in top0th or top25th) and losingt in top90th:
        gamescore += 3

    if (winningt in (top90th or top75th)) and losingt in newlypromo:
        gamescore -= 2
    if (winningt in (top90th or top75th)) and (losingt in top0th or top25th):
        gamescore -= 1
    '''
    if gamescore < 0:
        gamescore = 0
    print('Points:',gamescore,'\n')
print('Done')
