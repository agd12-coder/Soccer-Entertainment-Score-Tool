lst2 = list()
for val, key in lst1:
    tup2 = (val, key) - (val) + 1
    lst2.append(tup2)

for val, key in lst2:
    print (val, key) #line 58 under lst1 for loop.

posShot=shot_events[shot_events['result'].str.contains("Goal")]
print(posShot.head())
print(len(posShot)) #returns number of goals scored in total all season.

"""
number_games_played=input('Enter matchweek number/games played, or type "latest": ')

if number_games_played == 'latest' or 'Latest': #need to add still
    quit() 
else:
    try:
        number_games_played(float)
    except:
        print('Error. Try input again.')
        quit()

"""