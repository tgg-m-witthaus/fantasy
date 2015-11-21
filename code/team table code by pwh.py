# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%matplotlib inline
import pandas as pd
import numpy as np
import math as math
import requests
import csv
pd.set_option("display.max_columns",25)

from IPython.core.display import HTML
from bs4 import BeautifulSoup

# <codecell>

cd H:\git\fantasy\data

# <codecell>

current_week = 10

# <codecell>

# Yardage table

data = []

for wk in range(1, current_week): 
    r = requests.get("http://www.foxsports.com/nfl/stats?season=2015&seasonType=1&week=%d"%(wk)+"&category=YARDAGE&team=1&opp=0&sort=0&qualified=0")
    soup = BeautifulSoup(r.content)

    list = []
    
    for num in soup.find_all("tr")[2:]:    
        rows = [ele.text.strip() for ele in num.find_all("td")]
        list.append(rows)
    df = pd.DataFrame(list, columns = ['rank','team','tot_yds','ru_yds','ru_avg','ru_td','pa_yds','pa_yds/att','pa_yds/catch','pa_td','kr_yds','pr_yds','pen_yds'])
    df['week'] = wk
        
    data.append(df)
        

# Export to csv
yardage = pd.concat(data, axis = 0)
# yardage.to_csv('yardage.csv', index = False)

# <codecell>

# Passing table

data = []

for wk in range(1, current_week): 
    r = requests.get("http://www.foxsports.com/nfl/stats?season=2015&seasonType=1&week=%d"%(wk)+"&category=PASSING&team=1&opp=0&sort=0&qualified=0")
    soup = BeautifulSoup(r.content)

    list = []
    
    for num in soup.find_all("tr")[1:]:    
        rows = [ele.text.strip() for ele in num.find_all("td")]
        list.append(rows)
    df = pd.DataFrame(list, columns = ['rank','team','pa_comp','pa_att','pa_pct','pa_yds','pa_yds/att','pa_yds/rec','pa_td','pa_int','pa_qbr','pa_sacks','pa_yds_lost_sack','pa_fd','tot_fum','fum_lost'])
    df['week'] = wk
        
    data.append(df)
        

# Export to csv
passing = pd.concat(data, axis = 0)
# passing.to_csv('passing.csv', index = False)

# <codecell>

# Downs table

data = []

for wk in range(1, current_week): 
    r = requests.get("http://www.foxsports.com/nfl/stats?season=2015&seasonType=1&week=%d"%(wk)+"&category=DOWNS&team=1&opp=0&sort=0&qualified=0")
    soup = BeautifulSoup(r.content)

    list = []
    
    for num in soup.find_all("tr")[2:]:    
        rows = [ele.text.strip() for ele in num.find_all("td")]
        list.append(rows)
    
    df = pd.DataFrame(list, columns = ['rank','team','first_tot','first_rush','first_pass','third_conv','third_att','third_pct','fourth_conv','fourth_att','fouth_pct','pen_num','pen_for_first','pen_yds'])
    df['week'] = wk
    data.append(df)
        

# Export to csv
downs = pd.concat(data, axis = 0)
# downs.to_csv('downs.csv', index = False)

# <codecell>

# Rushing table

data = []

for wk in range(1, current_week): 
    r = requests.get("http://www.foxsports.com/nfl/stats?season=2015&seasonType=1&week=%d"%(wk)+"&category=RUSHING&team=1&opp=0&sort=0&qualified=0")
    soup = BeautifulSoup(r.content)

    list = []
    
    for num in soup.find_all("tr")[1:]:    
        rows = [ele.text.strip() for ele in num.find_all("td")]
        list.append(rows)
    
    df = pd.DataFrame(list, columns = ['rank','team','ru_att','ru_yds','ru_avg','ru_td','ru_first'])
    df['week'] = wk
    data.append(df)
        

# Export to csv
rush = pd.concat(data, axis = 0)
# rush.to_csv('rush.csv', index = False)

# <codecell>

# Turnover table

data = []

for wk in range(1, current_week): 
    r = requests.get("http://www.foxsports.com/nfl/stats?season=2015&seasonType=1&week=%d"%(wk)+"&category=TURNOVERS&team=1&opp=0&sort=0&qualified=0")
    soup = BeautifulSoup(r.content)

    list = []
    
    for num in soup.find_all("tr")[2:]:    
        rows = [ele.text.strip() for ele in num.find_all("td")]
        list.append(rows)
    
    df = pd.DataFrame(list, columns = ['to_rank','team','to_plus_minus','to_takeaway_int','to_takeaway_fum','to_giveaway_int','to_giveaway_fum'])
    df['week'] = wk
    data.append(df)
        

# Export to csv
turnovers = pd.concat(data, axis = 0)
# turnovers.to_csv('turnovers.csv', index = False)

# <codecell>

# Let's merge

data = pd.merge(rush, turnovers, on = ['team','week'],how='outer')
data = pd.merge(data, passing, on = ['team','week'],how='outer')
data = pd.merge(data, downs, on = ['team','week'],how='outer')
data = pd.merge(data, yardage, on = ['team','week'],how='outer')

# <codecell>

# Now let's add a couple more columns:

data['off_plays'] = data['ru_att'].astype(float) +  data['pa_att'].astype(float)
data['pct_plays_pa'] = data['pa_att'].astype(float) / data['off_plays'] 
data['pct_plays_ru'] = data['ru_att'].astype(float) / data['off_plays']

# And convert names to our initials naming convention
# data['team'] = data['team'].replace('San Francisco49ers','SF')

data['team'] = data['team'].replace({ 
                               'San Francisco49ers':'SF',
                               'BuffaloBills' : 'BUF',
                               'New YorkJets': 'NYJ',
                               'CarolinaPanthers': 'CAR',
                               'AtlantaFalcons': 'ATL',
                               'ChicagoBears': 'CHI',
                               'Kansas CityChiefs': 'KC',
                               'SeattleSeahawks': 'SEA',
                               'TennesseeTitans': 'TEN',
                               'CincinnatiBengals': 'CIN',
                               'Green BayPackers': 'GB',
                               'San DiegoChargers': 'SD',
                               'ClevelandBrowns': 'CLE',
                               'St. LouisRams': 'STL',
                               'Tampa BayBuccaneers': 'TB',
                               'PittsburghSteelers': 'PIT',
                               'ArizonaCardinals': 'ARI',
                               'DenverBroncos': 'DEN',
                               'New EnglandPatriots': 'NWE',
                               'New YorkGiants': 'NYG',
                               'BaltimoreRavens': 'BAL',
                               'DallasCowboys': 'DAL',
                               'HoustonTexans': 'HOU',
                               'JacksonvilleJaguars': 'JAC',
                               'New OrleansSaints': 'NOR',
                               'MiamiDolphins': 'MIA',
                               'IndianapolisColts': 'IND',
                               'MinnesotaVikings': 'MIN',
                               'DetroitLions': 'DET',
                               'OaklandRaiders': 'OAK',
                               'PhiladelphiaEagles': 'PHI',
                               'WashingtonRedskins': 'WAS'
                               
                               })

data

# <codecell>

# Print the master baby to a CSV
data.to_csv('team_table.csv', index = False)

# <codecell>

                                    'BuffaloBills', 'BUF',
                                    'New YorkJets', 'NYJ',
                                    'CarolinaPanthers', 'CAR',
                                    'AtlantaFalcons', 'ATL',
                                    'ChicagoBears', 'CHI',
                                    'Kansas CityChiefs', 'KC',
                                    'SeattleSeahawks', 'SEA',
                                    'TennesseeTitans', 'TEN',
                                    'CincinnatiBengals', 'CIN',
                                    'Green BayPackers', 'GB',
                                    'San DiegoChargers', 'SD',
                                    'ClevelandBrowns', 'CLE',
                                    'St. LouisRams', 'STL',
                                    'Tampa BayBuccaneers', 'TB',
                                    'PittsburghSteelers', 'PIT',
                                    'ArizonaCardinals', 'ARI',
                                    'DenverBroncos', 'DEN',
                                    'New EnglandPatriots', 'NWE',
                                    'New YorkGiants', 'NYG',
                                    'BaltimoreRavens', 'BAL',
                                    'DallasCowboys', 'DAL',
                                    'HoustonTexans', 'HOU',
                                    'JacksonvilleJaguars', 'JAC',
                                    'New OrleansSaints', 'NOR',
                                    'MiamiDolphins', 'MIA',
                                    'IndianapolisColts', 'IND',
                                    'MinnesotaVikings', 'MIN',
                                    'DetroitLions', 'DET',
                                    'OaklandRaiders', 'OAK',
                                    'PhiladelphiaEagles', 'PHI'

