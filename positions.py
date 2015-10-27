import os
from pandas import Series, DataFrame
import pandas as pd
import statsmodels.formula.api as sm

os.chdir(r"C:\fantasy")
f = pd.read_csv("salary and performance and odds.csv")
df = DataFrame(f)

result = sm.ols(formula="dk_points ~ dk_salary", data=df).fit()
print result.params
print result.summary()

