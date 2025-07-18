#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 18:55:29 2022

@author: umamazillur
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from linearmodels.panel import PanelOLS
from linearmodels import RandomEffects
from linearmodels.panel import PooledOLS


from ipumspy import readers, ddi
from pathlib import Path
from ipumspy import IpumsApiClient, UsaExtract, readers, ddi


pd.set_option('display.float_format', lambda x: '%.5f' % x)

# LOAD DATA
path = r'/Users/umamazillur/Documents/GitHub/final-project-dpii_final_uz_sb_am/Data'
os.chdir(path)

fname = 'IPUMS_data.csv'
fname_occ = 'occupationdict.xlsx'

ipums = pd.read_csv(os.path.join(path, fname))
occu_dict = pd.read_excel((os.path.join(path, fname_occ)), header = 0)

# CLEAN DATA

# drop household level variables 
drops = ['CBSERIAL', 'METAREAD', 'STRATA','GQ','HHWT', 'CLUSTER', 
         'PERNUM', 'PERWT', 'EDUCD']
ipums = ipums.drop(drops,axis = 1)

# create dictionaries to replace IPUMS variable codes with descriptive labels
occu_dict = dict(zip(occu_dict['Key'], occu_dict['Value']))
educ_dict = {6: 'educ_hs', 7: 'EDUC1', 8: 'EDUC2', 9: 'EDUC3', 10: 
             'EDUC4', 11:'EDUC5'}
ipums['OCC1950_NEW'] = ipums['OCC1950'].map(occu_dict) 
ipums['EDUC_NEW'] = ipums['EDUC'].map(educ_dict) 

# change gender variable to binary
ipums['FEMALE'] = np.where(ipums['SEX'] == 1, 0, 1)


# function to replace IPUMS region codes with descriptive labels
def region(x):
  if x == 11 or x == 12 or x == 13:
      return 'NORTHEAST'
  elif x == 21 or x == 22 or x == 23:
      return 'MIDWEST'
  elif x == 31 or x == 32 or x == 33 or x == 34:
      return 'SOUTH'
  else:
      return 'WEST'

# function to transform weekly and hourly wage interval data to average values
def weeks(x):
  if x == 1:
      return (1+13)/2
  elif x == 2:
      return (14+26)/2
  elif x == 3:
      return (27+39)/2
  elif x == 4:
      return (40+47)/2
  elif x == 5:
      return (48+49)/2
  else:
      return (50+52)/2

def hours(x):
  if x == 1:
      return (1+14)/2
  elif x == 2:
      return (15+29)/2
  elif x == 3:
      return (30+34)/2
  elif x == 4:
      return (35+39)/2
  elif x == 5:
      return 40
  elif x == 6:
      return (41+48)/2
  elif x == 7:
      return (49+59)/2
  else:
      return 64
  
def industry(x):
  if 100 < x < 200:
      return 1
  elif 200 < x < 300:
      return 2
  elif 300 < x < 400:
      return 3
  elif 400 < x < 500:
      return 4
  elif 500 < x < 600:
      return 5
  elif 600 < x < 700:
      return 6
  elif 700 < x < 800:
      return 7
  elif 800 < x < 900:
      return 8
  else:
      return 9
  
def gender(x):
  if 0 < x <= 0.33:
      return 'male'
  elif 0.67 <= x <= 1:
      return 'female'
  else:
      return 'mixed'
  
ipums['NEW REGION'] = ipums['REGION'].apply(region)
ipums['WEEKSWRK'] = ipums['WKSWORK2'].apply(weeks)
ipums['HOURSWRK'] = ipums['HRSWORK2'].apply(hours)
ipums['NEW_IND50'] = ipums['IND1950'].apply(industry)


# calculate hourly wage from weekly wage and hours worked data 
ipums['HRLYWAGE'] = (ipums['INCWAGE']/ipums['WEEKSWRK'])/ipums['HOURSWRK']
ipums['INF99_HRLYWAGE'] = ipums['HRLYWAGE']*ipums['CPI99']
# drop rows where wage is 0 
ipums = ipums[ipums.INF99_HRLYWAGE > 0]
# log wage variable 
ipums['LOG_WAGE'] = np.log(ipums['INF99_HRLYWAGE'])

# group dataset and get median wage data of each occupation
wage = ipums.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["LOG_WAGE"]].median()
wage = wage.rename(columns = {'LOG_WAGE': "LOG_MEDIAN_WAGE"})


# group dataset and calculate female to male ratio for each occupation
fem_ratio = ipums.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["FEMALE"]].sum()
fem_ratio = fem_ratio.rename(columns = {'FEMALE': 'FEMALE_COUNT'})
fem_ratio["COUNT"] = ipums.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["FEMALE"]].count()
fem_ratio["FEM_RATIO"] = (fem_ratio["FEMALE_COUNT"])/(fem_ratio["COUNT"])
fem_ratio['OCC_GENDER'] = fem_ratio['FEM_RATIO'].apply(gender)


# create dataframes with number of occupations in each region and education level
region_ratio = ipums.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["NEW REGION"]].value_counts()
region_ratio = region_ratio.to_frame()
region_ratio = region_ratio.reset_index()


region_ratio = region_ratio.pivot(index=['OCC1950_NEW', 'NEW_IND50', 'YEAR'], 
                                      columns = 'NEW REGION',
                                      values = 0 ) 

educ_ratio =  ipums.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["EDUC_NEW"]].value_counts()
educ_ratio = educ_ratio.to_frame()
educ_ratio = educ_ratio.reset_index()

educ_ratio = educ_ratio.pivot(index=["OCC1950_NEW", "NEW_IND50", "YEAR"], 
                                      columns = 'EDUC_NEW',
                                      values = 0) 


ipums_merged = pd.merge(region_ratio, educ_ratio, 
                     how = 'right', 
                     on = ["OCC1950_NEW", "NEW_IND50", "YEAR"])

ipums_merged = pd.merge(ipums_merged, fem_ratio, 
                    how = 'right', 
                    on = ["OCC1950_NEW", "NEW_IND50", "YEAR"])
ipums_merged = ipums_merged.reset_index()

# Use "COUNT" variable that stores total number of unique occupation-industry 
# pairs in each year to calculate ratio of occupations in each education level
# and across regions
ipums_merged["MIDWEST"] = (ipums_merged["MIDWEST"])/(ipums_merged["COUNT"])
ipums_merged["SOUTH"] = (ipums_merged["SOUTH"])/(ipums_merged["COUNT"])
ipums_merged["NORTHEAST"] = (ipums_merged["NORTHEAST"])/(ipums_merged["COUNT"])
ipums_merged["WEST"] = (ipums_merged["WEST"])/(ipums_merged["COUNT"])


ipums_merged["EDUC1"] = (ipums_merged["EDUC1"])/(ipums_merged["COUNT"])
ipums_merged["EDUC2"] = (ipums_merged["EDUC2"])/(ipums_merged["COUNT"])
ipums_merged["EDUC3"] = (ipums_merged["EDUC3"])/(ipums_merged["COUNT"])
ipums_merged["EDUC4"] = (ipums_merged["EDUC4"])/(ipums_merged["COUNT"])
ipums_merged["EDUC5"] = (ipums_merged["EDUC5"])/(ipums_merged["COUNT"])
ipums_merged["educ_hs"] = (ipums_merged["educ_hs"])/(ipums_merged["COUNT"])

# final dataframe to be used for analysis
ipums_final = pd.merge(ipums_merged, wage, 
                    how = 'right', 
                    on = ["OCC1950_NEW", "NEW_IND50", "YEAR"])
ipums_final.to_csv(r'/Users/umamazillur/Documents/GitHub/final-project-dpii_final_uz_sb_am/Data/ipums_final.csv')

# PLOTS

# PLOT 1: OCCUPATION GENDER DISTRIBUTION
occu_dist = ipums_final.groupby(['YEAR', 'OCC_GENDER']).count()
occu_dist = occu_dist.reset_index()
occu_dist = occu_dist[["YEAR", "OCC_GENDER", "COUNT"]]

occu_dist = occu_dist.pivot(index=['YEAR'], 
                                      columns = 'OCC_GENDER',
                                      values = 'COUNT' ) 
occu_dist = occu_dist.reset_index()
occu_dist["TOTAL"] = occu_dist["female"]+occu_dist["male"]+occu_dist["mixed"]
occu_dist["mixed"] = occu_dist["mixed"]/occu_dist["TOTAL"]
occu_dist["female"] = occu_dist["female"]/occu_dist["TOTAL"]
occu_dist["male"] = occu_dist["male"]/occu_dist["TOTAL"]
occu_dist = occu_dist.drop(["TOTAL"],  axis=1)


fig, ax = plt.subplots(figsize=(8,15))
sns.set(palette = 'Set2')
sns.set_style('whitegrid')
ax = occu_dist.plot(x='YEAR', kind='bar', stacked=True,
        title='Stacked Bar Graph by dataframe')
ax.legend(title='Occupation Gender')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
ax.set(xlabel='Year',
       ylabel= 'Occupation Gender',
       title='Occupation Gender Distribution')
plt.show
plt.savefig(r'/Users/umamazillur/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/occ_gend_dist.png', bbox_inches = 'tight')


#PLOT 2: OCCUPATION FEMINIZATION
gender_wage = pd.merge(ipums_merged, ipums, 
                    how = 'right', 
                    on = ["OCC1950_NEW", "NEW_IND50", "YEAR"])

female_wage = gender_wage[gender_wage["FEMALE"] == 1]
male_wage = gender_wage[gender_wage["FEMALE"] == 0]

fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
fig.suptitle('Impact of Occupation Feminization on Wages')
sns.set(palette = 'Set2')
sns.set_style('whitegrid')
sns.lineplot(ax=axes[0], x='YEAR', y="LOG_WAGE", data = female_wage, hue='OCC_GENDER',
             style= 'OCC_GENDER', markers=True, markersize = 10)
axes[0].set_title('FEMALE WAGE TREND')
axes[0].legend(title='Occupation Gender')
axes[0].grid(False)
sns.lineplot(ax=axes[1], x='YEAR', y="LOG_WAGE", data = male_wage, hue='OCC_GENDER',
            style= 'OCC_GENDER', markers=True, markersize = 10)
axes[1].set_title('MALE WAGE TREND')
axes[1].legend(title='Occupation Gender')
axes[1].grid(False)
plt.show
plt.savefig(r'/Users/umamazillur/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/occ_fem_wage.png')


#REGRESSION
    
# SIMPLE OLS MODEL    
ipums_final = ipums_final.dropna()

X = ipums_final[["FEM_RATIO", "YEAR"]]
y = ipums_final[["LOG_MEDIAN_WAGE"]]

mod = sm.OLS(y, sm.add_constant(X))
res = mod.fit()
res.summary()


mean_femratio = ipums_final.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["FEM_RATIO"]].mean()
median_wage = ipums_final.groupby(["OCC1950_NEW", "NEW_IND50","YEAR"])[["LOG_MEDIAN_WAGE"]].median()

X1 = mean_femratio["FEM_RATIO"].values[:,np.newaxis]
y1 = median_wage["LOG_MEDIAN_WAGE"].values

model2 = LinearRegression()
model2.fit(X1, y1)

# create scatterplot with regression line
fig, ax = plt.subplots(figsize=(8, 8))
plt.scatter(X1, y1, c ="yellow", edgecolor ="red")
plt.plot(X1, model2.predict(X1),color='k')
plt.xlabel("RATIO OF FEMALES IN AN OCCUPATION")
plt.ylabel("MEDIAN LOG WAGE")
plt.title("OLS RESULTS")
plt.show()
fig.savefig(r'/Users/umamazillur/Documents/GitHub/final-project-dpii_final_uz_sb_am/Images/OLS_results.png')


# FIXED EFFECTS MODEL 

reg_data = ipums_final.groupby(["OCC_GENDER","YEAR"]).mean()
reg_data = reg_data.reset_index()

year = pd.Categorical(reg_data.YEAR)
reg_data = reg_data.set_index(["OCC_GENDER", "YEAR"])
reg_data["year"] = year

exog_vars = ["FEM_RATIO"]
exog = sm.add_constant(reg_data[exog_vars])
mod = PooledOLS(reg_data['LOG_MEDIAN_WAGE'], exog)
pooled_res = mod.fit()
print(pooled_res)

# 1. https://stackoverflow.com/questions/22381497/python-scikit-learn-linear-model-parameter-standard-error
# 2. https://stackoverflow.com/questions/40941542/using-scikit-learn-linearregression-to-plot-a-linear-fit
# 3. https://dev.to/thalesbruno/subplotting-with-matplotlib-and-seaborn-5ei8
# 4. https://www.geeksforgeeks.org/ordinary-least-squares-ols-using-statsmodels/
# 5. https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions
# 6. https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_stata.html