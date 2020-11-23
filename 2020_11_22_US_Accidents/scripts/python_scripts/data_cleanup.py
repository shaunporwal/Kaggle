# -*- coding: utf-8 -*-
"""
#Script for data cleanup of US Accident data

Created on Mon Apr 20 21:11:18 2020
@author: keino
"""
### Description of US Countrywide Traffic Accident Dataset(2016 - 2019)
# Source: https://www.kaggle.com/sobhanmoosavi/us-accidents/download

# Import Required Libraries
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc3 as pm
import tensorflow as tf
import scipy.stats as stats
import datetime
import nltk
from IPython.display import display
import statsmodels.api as sm
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

## Load the dataset
#sys.path.append('/content/drive/My Drive/MSSM/ML_for_BDS')   #change working directory
db = pd.read_csv('/Users/ShaunPorwal/Desktop/sinai_classes/BMI3002_ML_2020/MLProject/US_Accidents_Dec19.csv')

### Step #1. Fix Date and Time Columns
#Since there is time and date columns, we can make it easier to work with (taken from Ismael)
# Convert Start_Time and End_Time to datetypes
db['Start_Time'] = pd.to_datetime(db['Start_Time'], errors='coerce')
db['End_Time'] = pd.to_datetime(db['End_Time'], errors='coerce')

# Extract year, month, day, hour and weekday
db['Year']=db['Start_Time'].dt.year
db['Month']=db['Start_Time'].dt.strftime('%b')
db['Day']=db['Start_Time'].dt.day
db['Hour']=db['Start_Time'].dt.hour
db['Weekday']=db['Start_Time'].dt.strftime('%a')

# Extract the amount of time in the unit of minutes for each accident, 
# round to the nearest integer
td='Time_Duration(min)'
db[td]=round((db['End_Time']-db['Start_Time'])/np.timedelta64(1,'m'))
db.info()

# Drop the rows with td<0
neg_outliers=db[td]<=0

# Drop rows with negative td
db.dropna(subset=[td],axis=0,inplace=True)

# Double check to make sure no more negative td
db[td].loc[(db[td]>=0)]

#Check missing remaining
print(db.isnull().sum())

### Step #2. Deal with tricky geography columns
#Drop End LAt and End Lng, since too many are missing and are hard to impute.
#They add little value
db.drop(labels=['End_Lat', 'End_Lng'],axis=1,inplace=True)

#Fill missing street number with a zero
db['Number'] = db['Number'].fillna(0)

#Impute the timezone, Zipcode and Airport_Code based on the State column
db['Timezone'] = db.groupby('State')['Timezone'].transform(lambda tz: tz.fillna(tz.value_counts().index[0]))
db['Zipcode'] = db.groupby('State')['Zipcode'].transform(lambda zc: zc.fillna(zc.value_counts().index[0]))
db['Airport_Code'] = db.groupby('State')['Airport_Code'].transform(lambda ac: ac.fillna(ac.value_counts().index[0]))

#Impute missing city uing most occuring states
db['City'] = db.groupby('State')['City'].transform(lambda grp: grp.fillna(grp.value_counts().index[0]))

#Check missing remaining
print(db.isnull().sum())

### Step #3. Fix all weather related columns
# Fill in NaN with mean values where appropriate
fill = ['Temperature(F)','Pressure(in)', 'Humidity(%)','Precipitation(in)', 'Wind_Chill(F)', 'Wind_Speed(mph)', 'Visibility(mi)']
for f in fill:
    db[f]=db[f].fillna(db[f].mean())

### Step #4. Fix all other columns   
#Impute time of day-sih columns 
def median_imputer(x):
    db[x].fillna(db[x].mode()[0],inplace=True)

median_impute = ['Sunrise_Sunset','Civil_Twilight','Astronomical_Twilight','Wind_Direction','Weather_Condition']
for col in median_impute:
    median_imputer(col)
    
# Impute Nautical Twilight, using start time
def fill(db,columns):
    lst = db[db[columns].isna()].index
    for i in lst:
        if 6<= db.loc[i,'Start_Time'].hour and db.loc[i,'Start_Time'].hour <18:
            db[columns] = db[columns].fillna('Day')
        else:
            db[columns] = db[columns].fillna('Night')

fill(db,'Nautical_Twilight')

#weather stamp not really important but can imput by using start time
db.loc[(pd.isnull(db.Weather_Timestamp)), 'Weather_Timestamp'] = db.Start_Time

#Fill one record in Description with the word 'Accident' #can fill later with most occuring word
db.Description = db.Description.fillna('Accident')

#Check missing remaining
print(db.isnull().sum())

#Set up data for Feature Selection 
X = db.drop("Severity",1)   #Feature Matrix
y = db["Severity"]          #Target Variable
db.head(2)


