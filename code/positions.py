import os
from pandas import Series, DataFrame
import pandas as pd
import concat
import statsmodels.formula.api as sm

os.chdir(r"C:\fantasy\data")
qb = pd.read_csv("RB Data.csv")
df_qb = DataFrame(qb)

# sort by player and week, also let's only keep 2015 for now
df_qb = df_qb[df_qb.year == 2015]
df_qb_sort = df_qb.sort_values(['Player','week'])

df_qb_sort.head()

points_rolling = pd.concat([df_qb_sort.Player, df_qb_sort["h/a"], df_qb_sort.week, df_qb_sort.dk_salary, df_qb_sort.total, df_qb_sort.dk_points, df_qb_sort.groupby('Player').dk_points.shift(), df_qb_sort.groupby('Player').dk_points.shift(2), df_qb_sort.groupby('Player').dk_points.shift(3)], axis=1)
list(df_qb)
points_rolling.columns = ['Player', 'home', 'week','dk_salary','total','dk_points','lag_one','lag_two','lag_three']

points_rolling_week6 = points_rolling[points_rolling.week==6]

result = sm.ols(formula="dk_points ~ home + dk_salary + total + lag_one + lag_two + lag_three", data=points_rolling).fit()
print result.params
print result.summary()
result.predict()

points_rolling_week7 = points_rolling[points_rolling.week==7]

points_rolling_week7.to_csv("rb_scores.csv")



#result = sm.ols(formula="fd_salary ~ total", data=df_qb).fit()
#print result.params
#print result.summary()

