#Assignment 4
#Description
#In this assignment you must read in a file of metropolitan regions and associated sports teams from assets/wikipedia_data.html
#and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the 
#"Big 4": NFL (football, in assets/nfl.csv), MLB (baseball, in assets/mlb.csv), NBA (basketball, in assets/nba.csv or 
#NHL (hockey, in assets/nhl.csv). Please keep in mind that all questions are from the perspective of the 
#metropolitan region, and that this file is the "source of authority" for the location of a given sports team. 
#Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan 
#region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've 
#been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!


#For each sport I would like you to answer the question: what is the win/loss ratio's correlation with the population of the 
#city it is in? Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember 
#that to calculate the correlation with pearsonr, so you are going to send in two ordered lists of values, the populations 
#from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios 
#for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment 
#(20%*4=80%) of the grade for this assignment. You should only use data from year 2018 for your analysis -- this is 
#important!


#Notes
#1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this 
#assignment.
#2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the 
#majority of grades for this assignment. This is by design!
#3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and 
#sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to 
#teams, or regexes which will clean up names).
#4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!


#Question 1
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.
import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nhl_correlation(): 
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    #remove anything in brackets
    cities['NHL'] = cities['NHL'].str.replace('\[.+\]','') #.replace('—',np.nan).replace('',np.nan).dropna()

    #split out the teams when there are multiples in a cell
    def split_teams(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z].+\s[A-Z].+|[A-Z][a-z]+', ini_str)
        return res_list

    #split teams into arrays
    cities['NHL'] = cities['NHL'].apply(lambda x: split_teams(x))


    #make a list of cities, teams, and populations
    #break arrays into individual rows for each team
    nhl_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 
    i = 0
    r = 0

    while i < cities['NHL'].count():
        j=0
        while j < len(cities.loc[i,'NHL']):
            nhl_map_df.loc[r,'Team'] = cities.loc[i,'NHL'][j] # get team(s)
            nhl_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
            nhl_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
            j+=1
            r+=1
        i+=1

    #split city
    def split_city(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
        return res_list

    #one word or start two words with a space between or one word and dash or one word and comma
    nhl_map_df['new_city'] = nhl_map_df['City'].apply(lambda x: split_city(x))
    nhl_map_df['city_team'] = nhl_map_df['new_city'] + ' ' + nhl_map_df['Team']


    #drop division rows without team data    
    nhl_df = nhl_df[~nhl_df['team'].str.contains('Division')]

    #remove asterisk from team names
    nhl_df['team'] = nhl_df['team'].str.replace('*','')

    #find win percentage referred to as win:loss ratio in instructions
    nhl_df['w_l_ratio'] = nhl_df['W'].astype(int) / (nhl_df['W'].astype(int) + nhl_df['L'].astype(int))

    #2018 data only
    nhl_df = nhl_df[nhl_df['year']==2018]

    #map the stragglers
    teamDict = {'New York Devils':'New Jersey Devils','San Francisco Sharks':'San Jose Sharks',
                'Minneapolis Wild':'Minnesota Wild','Denver Avalanche':'Colorado Avalanche',
                'Miami Panthers':'Florida Panthers','Phoenix Coyotes':'Arizona Coyotes',
                'St Blues':'St. Louis Blues','Las Vegas Golden Knights':'Vegas Golden Knights',
                'Raleigh Hurricanes':'Carolina Hurricanes','Los Angeles Ducks':'Anaheim Ducks'
                ''}

    nhl_map_df['city_team'] = nhl_map_df['city_team'].replace(teamDict)


    #join datasets
    nhl_full_df = nhl_map_df.merge(nhl_df,how='left',left_on='city_team',right_on='team')

    corr_df = nhl_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    population_by_region = corr_df['Pop'].values.astype(float) # pass in metropolitan area population from cities
    win_loss_by_region = corr_df['w_l_ratio'].values.astype(float) # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


#Question 2¶
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NBA using 2018 data.

import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nba_correlation():
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]

    #remove anything in brackets
    cities['NBA'] = cities['NBA'].str.replace('\(.+\)','') #remove anything in parentheses

    #split out the teams when there are multiples in a cell
    def split_teams(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z].+\s[A-Z].+|[A-Z][a-z]+', ini_str)
        return res_list

    #split teams into arrays
    cities['NBA'] = cities['NBA'].apply(lambda x: split_teams(x))


    #make a list of cities, teams, and populations
    #break arrays into individual rows for each team
    nba_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 
    i = 0
    r = 0

    while i < cities['NBA'].count():
        j=0
        while j < len(cities.loc[i,'NBA']):
            nba_map_df.loc[r,'Team'] = cities.loc[i,'NBA'][j] # get team(s)
            nba_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
            nba_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
            j+=1
            r+=1
        i+=1

    #split city
    def split_city(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
        return res_list

    #one word or start two words with a space between or one word and dash or one word and comma
    nba_map_df['new_city'] = nba_map_df['City'].apply(lambda x: split_city(x))
    nba_map_df['city_team'] = nba_map_df['new_city'] + ' ' + nba_map_df['Team']

    #add missing 76ers
    seventy_sixer_df = pd.DataFrame({'City':['Philadelphia'],'Pop':['6070500'],
                                     'Team':['76ers'],'new_city': ['Philadelphia'],'city_team':['Philadelphia 76ers']})

    nba_map_df = nba_map_df.append(seventy_sixer_df,ignore_index=True)

    #drop division rows without team data    
    nba_df = nba_df[~nba_df['team'].str.contains('Division')]

    #remove asterisk from team names
    nba_df['team'] = nba_df['team'].str.replace('\(.+\)','')
    nba_df['team'] = nba_df['team'].str.replace('*','')
    nba_df['team'] = nba_df['team'].str.strip()

    #find win percentage referred to as win:loss ratio in instructions
    nba_df['w_l_ratio'] = nba_df['W'].astype(int) / (nba_df['W'].astype(int) + nba_df['L'].astype(int))

    #2018 data only
    nba_df = nba_df[nba_df['year']==2018]

    #map the stragglers
    teamDict = {'New York Nets':'Brooklyn Nets','San Francisco Warriors':'Golden State Warriors',
                'Minneapolis Timberwolves':'Minnesota Timberwolves','Indianapolis Pacers':'Indiana Pacers',
                'Salt Lake Jazz':'Utah Jazz'
               }

    nba_map_df['city_team'] = nba_map_df['city_team'].replace(teamDict)


    #join datasets
    nba_full_df = nba_map_df.merge(nba_df,how='left',left_on='city_team',right_on='team')

    corr_df = nba_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    population_by_region = corr_df['Pop'].values.astype(float) # pass in metropolitan area population from cities
    win_loss_by_region = corr_df['w_l_ratio'].values.astype(float) # pass in win/loss ratio from nba_ in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


#Question 3
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the MLB using 
import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def mlb_correlation(): 
    
    MLB_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]


    #remove anything in brackets
    cities['MLB'] = cities['MLB'].str.replace('\(.+\)','') #remove anything in parentheses
    cities['MLB'] = cities['MLB'].str.replace('\[.+\]','') #brackets

    def split_teams(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)
        return res_list

    #split teams into arrays
    cities['MLB'] = cities['MLB'].apply(lambda x: split_teams(x))

    #make a list of cities, teams, and populations
    #break arrays into individual rows for each team
    MLB_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 

    i = 0
    r = 0

    while i < cities['MLB'].count():
        j=0
        while j < len(cities.loc[i,'MLB']):
            MLB_map_df.loc[r,'Team'] = cities.loc[i,'MLB'][j] # get team(s)
            MLB_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
            MLB_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
            j+=1
            r+=1
        i+=1

    #split city
    def split_city(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
        return res_list

    #one word or start two words with a space between or one word and dash or one word and comma
    MLB_map_df['new_city'] = MLB_map_df['City'].apply(lambda x: split_city(x))
    MLB_map_df['city_team'] = MLB_map_df['new_city'] + ' ' + MLB_map_df['Team']

    #drop division rows without team data    
    MLB_df = MLB_df[~MLB_df['team'].str.contains('Division')]

    #remove asterisk from team names
    MLB_df['team'] = MLB_df['team'].str.replace('\(.+\)','')
    MLB_df['team'] = MLB_df['team'].str.replace('*','')
    MLB_df['team'] = MLB_df['team'].str.strip()

    #find win percentage referred to as win:loss ratio in instructions
    MLB_df['w_l_ratio'] = MLB_df['W'].astype(int) / (MLB_df['W'].astype(int) + MLB_df['L'].astype(int))

    #2018 data only
    MLB_df = MLB_df[MLB_df['year']==2018]

    #map the stragglers
    teamDict = {'San Francisco Athletics':'Oakland Athletics','Dallas Rangers':'Texas Rangers',
                'Minneapolis Twins':'Minnesota Twins','Denver Rockies':'Colorado Rockies',
                'Phoenix Diamondbacks':'Arizona Diamondbacks','St Cardinals':'St. Louis Cardinals'
               }


    MLB_map_df['city_team'] = MLB_map_df['city_team'].replace(teamDict)


    #join datasets
    MLB_full_df = MLB_map_df.merge(MLB_df,how='left',left_on='city_team',right_on='team')

    corr_df = MLB_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    population_by_region = corr_df['Pop'].values.astype(float) # pass in metropolitan area population from cities
    win_loss_by_region = corr_df['w_l_ratio'].values.astype(float) # pass in win/loss ratio from MLB_ in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]




#Question 4
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NFL using 2018 data.

import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nfl_correlation(): 

    NFL_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]


    #remove anything in brackets
    cities['NFL'] = cities['NFL'].str.replace('\(.+\)','') #remove anything in parentheses
    cities['NFL'] = cities['NFL'].str.replace('\[.+\]','') #brackets

    #clean nfl_df
    NFL_df['team'] = NFL_df['team'].str.replace('\+','') #brackets
    NFL_df['team'] = NFL_df['team'].str.replace('\*','') #brackets


    def split_teams(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)
        return res_list

    #split teams into arrays
    cities['NFL'] = cities['NFL'].apply(lambda x: split_teams(x))


    #make a list of cities, teams, and populations
    #break arrays into individual rows for each team
    NFL_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 

    i = 0
    r = 0

    while i < cities['NFL'].count():
        j=0
        while j < len(cities.loc[i,'NFL']):
            NFL_map_df.loc[r,'Team'] = cities.loc[i,'NFL'][j] # get team(s)
            NFL_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
            NFL_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
            j+=1
            r+=1
        i+=1


    #split city
    def split_city(ini_str):
        # Splitting on UpperCase using re
        res_list = []
        res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
        return res_list

    #one word or start two words with a space between or one word and dash or one word and comma
    NFL_map_df['new_city'] = NFL_map_df['City'].apply(lambda x: split_city(x))
    NFL_map_df['city_team'] = NFL_map_df['new_city'] + ' ' + NFL_map_df['Team']


    #drop division rows without team data    
    NFL_df = NFL_df[~NFL_df['team'].str.contains('AFC')]
    NFL_df = NFL_df[~NFL_df['team'].str.contains('NFC')]

    #remove asterisk from team names
    NFL_df['team'] = NFL_df['team'].str.replace('\(.+\)','')
    NFL_df['team'] = NFL_df['team'].str.replace('*','')
    NFL_df['team'] = NFL_df['team'].str.strip()


    #find win percentage referred to as win:loss ratio in instructions
    NFL_df['w_l_ratio'] = NFL_df['W'].astype(int) / (NFL_df['W'].astype(int) + NFL_df['L'].astype(int))

    #2018 data only
    NFL_df = NFL_df[NFL_df['year']==2018]

    #map the stragglers
    teamDict = {'San Francisco Raiders':'Oakland Raiders',
                'Boston Patriots':'New England Patriots',
                'Minneapolis Vikings':'Minnesota Vikings','Phoenix Cardinals':'Arizona Cardinals',
                'Charlotte Panthers':'Carolina Panthers',
                'Nashville Titans':'Tennessee Titans'   
               }


    NFL_map_df['city_team'] = NFL_map_df['city_team'].replace(teamDict)


    #join datasets
    NFL_full_df = NFL_map_df.merge(NFL_df,how='left',left_on='city_team',right_on='team')

    corr_df = NFL_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    population_by_region = corr_df['Pop'].values.astype(float) # pass in metropolitan area population from cities
    win_loss_by_region = corr_df['w_l_ratio'].values.astype(float) # pass in win/loss ratio from NFL_ in the same order as cities["Metropolitan area"]

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


#Question 5
#In this question I would like you to explore the hypothesis that given that an area has two sports teams in different sports,
#those teams will perform the same within their respective sports. How I would like to see this explored is with a series of 
#paired t-tests (so use ttest_rel) between all pairs of sports. Are there any sports where we can reject the null hypothesis? 
#Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, 
#cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this 
#assignment.

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def sports_team_performance():

    #===============NHL===============
    def NHL():
        nhl_df=pd.read_csv("assets/nhl.csv")
        cities=pd.read_html("assets/wikipedia_data.html")[1]
        cities=cities.iloc[:-1,[0,3,5,6,7,8]]
        #remove anything in brackets
        cities['NHL'] = cities['NHL'].str.replace('\[.+\]','') #.replace('—',np.nan).replace('',np.nan).dropna()

        #split out the teams when there are multiples in a cell
        def split_teams(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z].+\s[A-Z].+|[A-Z][a-z]+', ini_str)
            return res_list

        #split teams into arrays
        cities['NHL'] = cities['NHL'].apply(lambda x: split_teams(x))


        #make a list of cities, teams, and populations
        #break arrays into individual rows for each team
        nhl_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 
        i = 0
        r = 0

        while i < cities['NHL'].count():
            j=0
            while j < len(cities.loc[i,'NHL']):
                nhl_map_df.loc[r,'Team'] = cities.loc[i,'NHL'][j] # get team(s)
                nhl_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
                nhl_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
                j+=1
                r+=1
            i+=1

        #split city
        def split_city(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
            return res_list

        #one word or start two words with a space between or one word and dash or one word and comma
        nhl_map_df['new_city'] = nhl_map_df['City'].apply(lambda x: split_city(x))
        nhl_map_df['city_team'] = nhl_map_df['new_city'] + ' ' + nhl_map_df['Team']


        #drop division rows without team data    
        nhl_df = nhl_df[~nhl_df['team'].str.contains('Division')]

        #remove asterisk from team names
        nhl_df['team'] = nhl_df['team'].str.replace('*','')

        #find win percentage referred to as win:loss ratio in instructions
        nhl_df['w_l_ratio'] = nhl_df['W'].astype(int) / (nhl_df['W'].astype(int) + nhl_df['L'].astype(int))

        #2018 data only
        nhl_df = nhl_df[nhl_df['year']==2018]

        #map the stragglers
        teamDict = {'New York Devils':'New Jersey Devils','San Francisco Sharks':'San Jose Sharks',
                    'Minneapolis Wild':'Minnesota Wild','Denver Avalanche':'Colorado Avalanche',
                    'Miami Panthers':'Florida Panthers','Phoenix Coyotes':'Arizona Coyotes',
                    'St Blues':'St. Louis Blues','Las Vegas Golden Knights':'Vegas Golden Knights',
                    'Raleigh Hurricanes':'Carolina Hurricanes','Los Angeles Ducks':'Anaheim Ducks'
                    ''}

        nhl_map_df['city_team'] = nhl_map_df['city_team'].replace(teamDict)


        #join datasets
        nhl_full_df = nhl_map_df.merge(nhl_df,how='left',left_on='city_team',right_on='team')

        return nhl_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})


    #================NBA========================

    def NBA():
        nba_df=pd.read_csv("assets/nba.csv")
        cities=pd.read_html("assets/wikipedia_data.html")[1]
        cities=cities.iloc[:-1,[0,3,5,6,7,8]]

        #remove anything in brackets
        cities['NBA'] = cities['NBA'].str.replace('\(.+\)','') #remove anything in parentheses

        #split out the teams when there are multiples in a cell
        def split_teams(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z].+\s[A-Z].+|[A-Z][a-z]+', ini_str)
            return res_list

        #split teams into arrays
        cities['NBA'] = cities['NBA'].apply(lambda x: split_teams(x))


        #make a list of cities, teams, and populations
        #break arrays into individual rows for each team
        nba_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 
        i = 0
        r = 0

        while i < cities['NBA'].count():
            j=0
            while j < len(cities.loc[i,'NBA']):
                nba_map_df.loc[r,'Team'] = cities.loc[i,'NBA'][j] # get team(s)
                nba_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
                nba_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
                j+=1
                r+=1
            i+=1

        #split city
        def split_city(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
            return res_list

        #one word or start two words with a space between or one word and dash or one word and comma
        nba_map_df['new_city'] = nba_map_df['City'].apply(lambda x: split_city(x))
        nba_map_df['city_team'] = nba_map_df['new_city'] + ' ' + nba_map_df['Team']

        #add missing 76ers
        seventy_sixer_df = pd.DataFrame({'City':['Philadelphia'],'Pop':['6070500'],
                                         'Team':['76ers'],'new_city': ['Philadelphia'],'city_team':['Philadelphia 76ers']})

        nba_map_df = nba_map_df.append(seventy_sixer_df,ignore_index=True)

        #drop division rows without team data    
        nba_df = nba_df[~nba_df['team'].str.contains('Division')]

        #remove asterisk from team names
        nba_df['team'] = nba_df['team'].str.replace('\(.+\)','')
        nba_df['team'] = nba_df['team'].str.replace('*','')
        nba_df['team'] = nba_df['team'].str.strip()

        #find win percentage referred to as win:loss ratio in instructions
        nba_df['w_l_ratio'] = nba_df['W'].astype(int) / (nba_df['W'].astype(int) + nba_df['L'].astype(int))

        #2018 data only
        nba_df = nba_df[nba_df['year']==2018]

        #map the stragglers
        teamDict = {'New York Nets':'Brooklyn Nets','San Francisco Warriors':'Golden State Warriors',
                    'Minneapolis Timberwolves':'Minnesota Timberwolves','Indianapolis Pacers':'Indiana Pacers',
                    'Salt Lake Jazz':'Utah Jazz'
                   }

        nba_map_df['city_team'] = nba_map_df['city_team'].replace(teamDict)


        #join datasets
        nba_full_df = nba_map_df.merge(nba_df,how='left',left_on='city_team',right_on='team')

        return nba_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    #================MLB========================

    def MLB(): 

        MLB_df=pd.read_csv("assets/mlb.csv")
        cities=pd.read_html("assets/wikipedia_data.html")[1]
        cities=cities.iloc[:-1,[0,3,5,6,7,8]]


        #remove anything in brackets
        cities['MLB'] = cities['MLB'].str.replace('\(.+\)','') #remove anything in parentheses
        cities['MLB'] = cities['MLB'].str.replace('\[.+\]','') #brackets

        def split_teams(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)
            return res_list

        #split teams into arrays
        cities['MLB'] = cities['MLB'].apply(lambda x: split_teams(x))

        #make a list of cities, teams, and populations
        #break arrays into individual rows for each team
        MLB_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 

        i = 0
        r = 0

        while i < cities['MLB'].count():
            j=0
            while j < len(cities.loc[i,'MLB']):
                MLB_map_df.loc[r,'Team'] = cities.loc[i,'MLB'][j] # get team(s)
                MLB_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
                MLB_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
                j+=1
                r+=1
            i+=1

        #split city
        def split_city(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
            return res_list

        #one word or start two words with a space between or one word and dash or one word and comma
        MLB_map_df['new_city'] = MLB_map_df['City'].apply(lambda x: split_city(x))
        MLB_map_df['city_team'] = MLB_map_df['new_city'] + ' ' + MLB_map_df['Team']

        #drop division rows without team data    
        MLB_df = MLB_df[~MLB_df['team'].str.contains('Division')]

        #remove asterisk from team names
        MLB_df['team'] = MLB_df['team'].str.replace('\(.+\)','')
        MLB_df['team'] = MLB_df['team'].str.replace('*','')
        MLB_df['team'] = MLB_df['team'].str.strip()

        #find win percentage referred to as win:loss ratio in instructions
        MLB_df['w_l_ratio'] = MLB_df['W'].astype(int) / (MLB_df['W'].astype(int) + MLB_df['L'].astype(int))

        #2018 data only
        MLB_df = MLB_df[MLB_df['year']==2018]

        #map the stragglers
        teamDict = {'San Francisco Athletics':'Oakland Athletics','Dallas Rangers':'Texas Rangers',
                    'Minneapolis Twins':'Minnesota Twins','Denver Rockies':'Colorado Rockies',
                    'Phoenix Diamondbacks':'Arizona Diamondbacks','St Cardinals':'St. Louis Cardinals'
                   }


        MLB_map_df['city_team'] = MLB_map_df['city_team'].replace(teamDict)


        #join datasets
        MLB_full_df = MLB_map_df.merge(MLB_df,how='left',left_on='city_team',right_on='team')

        return MLB_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    #================NFL========================

    def NFL():

        NFL_df=pd.read_csv("assets/nfl.csv")
        cities=pd.read_html("assets/wikipedia_data.html")[1]
        cities=cities.iloc[:-1,[0,3,5,6,7,8]]


        #remove anything in brackets
        cities['NFL'] = cities['NFL'].str.replace('\(.+\)','') #remove anything in parentheses
        cities['NFL'] = cities['NFL'].str.replace('\[.+\]','') #brackets

        #clean nfl_df
        NFL_df['team'] = NFL_df['team'].str.replace('\+','') #brackets
        NFL_df['team'] = NFL_df['team'].str.replace('\*','') #brackets


        def split_teams(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)
            return res_list

        #split teams into arrays
        cities['NFL'] = cities['NFL'].apply(lambda x: split_teams(x))


        #make a list of cities, teams, and populations
        #break arrays into individual rows for each team
        NFL_map_df = pd.DataFrame([], columns = ['City', 'Pop', 'Team']) 

        i = 0
        r = 0

        while i < cities['NFL'].count():
            j=0
            while j < len(cities.loc[i,'NFL']):
                NFL_map_df.loc[r,'Team'] = cities.loc[i,'NFL'][j] # get team(s)
                NFL_map_df.loc[r,'City'] = cities.loc[i,'Metropolitan area'] # get city
                NFL_map_df.loc[r,'Pop'] = cities.loc[i,'Population (2016 est.)[8]'] # get population 
                j+=1
                r+=1
            i+=1


        #split city
        def split_city(ini_str):
            # Splitting on UpperCase using re
            res_list = []
            res_list = re.findall('[A-Z][a-z]+\s[A-Z][a-z]+|[A-Z][a-z]+', ini_str)[0]
            return res_list

        #one word or start two words with a space between or one word and dash or one word and comma
        NFL_map_df['new_city'] = NFL_map_df['City'].apply(lambda x: split_city(x))
        NFL_map_df['city_team'] = NFL_map_df['new_city'] + ' ' + NFL_map_df['Team']


        #drop division rows without team data    
        NFL_df = NFL_df[~NFL_df['team'].str.contains('AFC')]
        NFL_df = NFL_df[~NFL_df['team'].str.contains('NFC')]

        #remove asterisk from team names
        NFL_df['team'] = NFL_df['team'].str.replace('\(.+\)','')
        NFL_df['team'] = NFL_df['team'].str.replace('*','')
        NFL_df['team'] = NFL_df['team'].str.strip()


        #find win percentage referred to as win:loss ratio in instructions
        NFL_df['w_l_ratio'] = NFL_df['W'].astype(int) / (NFL_df['W'].astype(int) + NFL_df['L'].astype(int))

        #2018 data only
        NFL_df = NFL_df[NFL_df['year']==2018]

        #map the stragglers
        teamDict = {'San Francisco Raiders':'Oakland Raiders',
                    'Boston Patriots':'New England Patriots',
                    'Minneapolis Vikings':'Minnesota Vikings','Phoenix Cardinals':'Arizona Cardinals',
                    'Charlotte Panthers':'Carolina Panthers',
                    'Nashville Titans':'Tennessee Titans'   
                   }

        NFL_map_df['city_team'] = NFL_map_df['city_team'].replace(teamDict)

        #join datasets
        NFL_full_df = NFL_map_df.merge(NFL_df,how='left',left_on='city_team',right_on='team')

        return NFL_full_df.groupby('City').agg({'Pop': 'max','w_l_ratio':'mean'})

    #===============================================================
    #function to grab data for each sport for use in for loop
    def sport_frame(sport):
        if sport == 'NBA':
            return NBA()
        elif sport == 'MLB':
            return MLB()
        elif sport == 'NHL':
            return NHL()
        elif sport == 'NFL':
            return NFL()
        else:
            'error'
    #==================Do the calcs================================

    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)


    #loop through all team pairings
    for i in sports:
        for j in sports:
            merge_df = sport_frame(i).merge(sport_frame(j),how='inner',left_on='City',right_on='City')
            p_values.loc[i,j] = stats.ttest_rel(merge_df['w_l_ratio_x'], merge_df['w_l_ratio_y'])[1]
            
    return p_values
