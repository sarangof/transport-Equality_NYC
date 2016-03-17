# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:38:29 2016
"""

#import shapefile as shp
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab as pl
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as sp

IT_index = pd.DataFrame([])

""" 
IT_index is a data frame that will include all the components of our index.
This code is split among between the three components of the index.

"""


"""
Component A - transportation expenses versus income
"""

#

Income2013 = pd.read_csv('data/2013Incomepc.csv',  header=1, names=["id", "id2block", "block", "PCincome", "error"] , usecols=["id2block", "PCincome"])
Income2013.PCincome = Income2013.PCincome.replace("-", "0")
Income2013.PCincome = Income2013.PCincome.astype(int)
Mtrans2013 = pd.read_csv('data/Meanoftransportation.csv',  header=1, usecols=[1, 5, 21,37])
Mtrans2013.columns = ['id2block', 'Car', 'PTrans', 'Bike']
Mtrans2013['Tcommuters'] = Mtrans2013.Car + Mtrans2013.PTrans + Mtrans2013.Bike
Mtrans2013['Pcar'] = Mtrans2013.Car/Mtrans2013.Tcommuters
Mtrans2013['PPTrans'] = Mtrans2013.PTrans/Mtrans2013.Tcommuters
Mtrans2013['PBike'] = Mtrans2013.Bike/Mtrans2013.Tcommuters
Costcar2013 = pd.read_excel('data/norteastCES2013.xlsx',  header=1, usecols=["Item", "New York"])
Costcar2013 = Costcar2013[43:46]
Carcost = sum(Costcar2013["New York"])
Costptrans2013 = pd.read_excel('data/Publictransportationcosts.xlsx')
Costptrans2013['Pondcost'] = Costptrans2013.Porcentage*Costptrans2013['Value per trip']*Costptrans2013['Trips per year']
PTcost = sum(Costptrans2013.Pondcost)
Bcost = 95
CompA = pd.merge(Income2013, Mtrans2013, on=['id2block'])
CompA['CompA'] = np.log((CompA.Pcar*Carcost + CompA.PPTrans*PTcost + CompA.PBike*Bcost)/(CompA.PCincome))
CompA[CompA.CompA > 1]
CompA = CompA[CompA.CompA < 1]
CompA['CompA1'] = (CompA.CompA - CompA.CompA.min())/(CompA.CompA.max() - CompA.CompA.min())

#CompA.set_index(CompA['id2block'])
IT_index['CompA'] = CompA['CompA1']
#IT_index.set_index(Income2013.id2block)

"""
# Component B - time of commute
"""

timeW = pd.read_csv('data/timeWorkBG.csv',skiprows=2,names=[u'Id', u'Id2', u'Geography', u'E_Total', u'ME_Total',
       u'ET_5', u'ME_5', u'ET5_9', u'ME_9', 
       'ET_14', u'ME_14', u'ET_19', u'ME_19',
       u'ET_24',u'ME_24','ET_29', u'ME_29',
       u'ET_34',u'ME_34',u'ET_39',u'ME_39',
       u'ET_44',u'ME_44',u'ET_59',u'ME_59',
       u'ET_89',u'ME_89',u'ET_90m',u'ME_90m'])

avgTime = np.array([2.5,7,12,17,22,27,32,37,42,52,74,100])

timeW['av_time']  =  (timeW[[u'ET_5',u'ET5_9','ET_14',u'ET_19',u'ET_24','ET_29',u'ET_34',
                          u'ET_39',u'ET_44',u'ET_59',u'ET_89',u'ET_90m']]*avgTime).sum(axis=1)
timeW['av_time']  = timeW['av_time']/timeW['E_Total']
OD = pd.read_csv('data/ODjobs.csv')
OD=OD.rename(columns = {'h_geocode':'id2block'})

distW = pd.read_csv('data/dist.csv',names=['ind','av_distance'],usecols=['av_distance'],header=0)
distW['av_distance'] = distW['av_distance'].astype(np.float64)
IT_index['CompB']    = timeW['av_time']


timeW             = timeW.rename(columns = {'Id2':'id2block'})
IT_index          = pd.merge(timeW[['id2block','av_time']],CompA[['id2block','CompA1']],on = 'id2block')
IT_index          = IT_index.rename(columns = {'CompA1':'CompA'})
distW             = distW.set_index(IT_index['id2block'])
IT_index['av_distance'] = np.array(distW['av_distance'])
IT_index['CompB'] = IT_index['av_time'] / IT_index['av_distance']
IT_index['CompB'] = (IT_index['CompB']  - IT_index['CompB'].min()) / (IT_index['CompB'].max()-IT_index['CompB'].min())


"""
# Component C - Accesibility
author: Xia Wang
date: 03/08/2015
"""

# read the original Bus_Metro_Bike data
data = pd.read_csv('data/Bus_Metro.txt', header = 0)
databike = pd.read_csv('data/Bike_Bus_Metro.txt', header = 0)
# data.shape
data['Num_Metro_update'] = None
# update the number of metro for CBGs that are within the 0.25 mile buffer
for i in data.index:
    if data.ix[i,'Metro_Buff'] > data.ix[i, 'Num_Metro']:
        data.ix[i, 'Num_Metro_update'] = data.ix[i, 'Metro_Buff']
    elif data.ix[i, 'Num_Metro'] <= data.ix[i, 'Num_Metro']:
        data.ix[i, 'Num_Metro_update'] = data.ix[i, 'Num_Metro']

data['Num_Bus_update'] = None
# update the number of Bus for CBGs that are within the 0.25 mile buffer
for i in data.index:
    if data.ix[i,'Bus_Buff'] > data.ix[i, 'Num_Bus']:
        data.ix[i, 'Num_Bus_update'] = data.ix[i, 'Bus_Buff']
    elif data.ix[i, 'Num_Bus'] <= data.ix[i, 'Num_Bus']:
        data.ix[i, 'Num_Bus_update'] = data.ix[i, 'Num_Bus']
# create a new intermediate dataFrame with all and only the relevant columns        
data_clean = data[['CBG_id', 'Num_Metro_update','Num_Bus_update', 'BlockGroupArea']]
data_clean['CBG_id'].astype(str, inplace = True)
# data_clean.shape
# create a new dataFrame with bike length and Census Block Group ID
bike = databike[['CBG_id','BikeLength']]
# bike.head()
bike['CBG_id'].astype(str, inplace = True)
# if one block group has more than one section of bike lane, add all the length to that CBG
bike_agg = bike.groupby('CBG_id').aggregate(sum)
bike_agg.reset_index(inplace = True)
# bike_agg.head()
# combine the bike length and the Bus_Metro data
bike_merge = pd.merge(data_clean, bike_agg,
                      how = 'left',
                      on= 'CBG_id')
# bike_merge['CBG_id'].shape
# substitute the nans with 0 
bike_merge.replace(np.nan, 0, inplace = True)
# calculate the subindices for Bus, Metro and Bike Separately
# Bus_subindex
bike_merge['Bus_pre'] = bike_merge['Num_Bus_update']*1.0 / bike_merge['BlockGroupArea']
bike_merge['CompBus'] = ((bike_merge['Bus_pre']*1.0 - bike_merge['Bus_pre'].min()) / 
                          (bike_merge['Bus_pre'].max() - bike_merge['Bus_pre'].min()))
# Metro_subindex
bike_merge['Metro_pre'] = bike_merge['Num_Metro_update']*1.0 / bike_merge['BlockGroupArea']
bike_merge['CompMetro'] = ((bike_merge['Metro_pre']*1.0 - bike_merge['Metro_pre'].min()) / 
                          (bike_merge['Metro_pre'].max() - bike_merge['Metro_pre'].min()))
# Bike_subindex
bike_merge['Bike_pre'] = bike_merge['BikeLength'] / bike_merge['BlockGroupArea']
bike_merge['CompBike'] = ((bike_merge['Bike_pre']*1.0 - bike_merge['Bike_pre'].min()) / 
                          (bike_merge['Bike_pre'].max() - bike_merge['Bike_pre'].min()))

# combine the 3 subindices and give them equal weight
bike_merge['CompC'] = 0.3333 * bike_merge['CompBus'] + 0.3333 * bike_merge['CompMetro'] + 0.3333 * bike_merge['CompBike']
bike_merge['CompC_norm'] = ((bike_merge['CompC']*1.0 - bike_merge['CompC'].min()) / 
                             (bike_merge['CompC'].max() - bike_merge['CompC'].min()))
# build a dataFrame for index 3
CompC = bike_merge[['CBG_id','CompC', 'CompC_norm']]
CompC['CompC_norm'] = -CompC['CompC_norm'] + 1

 
CompC=CompC.rename(columns = {'CBG_id':'id2block'})
#IT_index['id2block'] = IT_index['id2block'].astype(str).str[1:].astype(np.int64)
# C3['CompC'] = (0.55*C3['Num_Metro_update'] + 0.45*C3['Num_Bus_update']) / C3['Shape_Area']
# C3['CompC'] = (C3['CompC'] - C3['CompC'].min()) / (C3['CompC'].max() - C3['CompC'].min() ) 
IT_index = pd.merge(CompC[['id2block','CompC_norm']],IT_index,on='id2block')
#
IT_index['total'] = 1.0/3*IT_index['CompA'] + 1.0/3*IT_index['CompB'] + 1.0/3*IT_index['CompC_norm']
#Plotting the results
ax1 = IT_index.total.hist(grid=True, figsize=(7,5), alpha=0.7)
ax1.set_xlabel("Score", fontsize = 11)
ax1.set_title("NYC Transportation Inequity Index", fontsize = 14)
IT_index.plot(x='CompA', y='CompB', kind='scatter')
IT_index.plot(x='CompA', y='CompC_norm', kind='scatter')
IT_index.plot(x='CompB', y='CompC_norm', kind='scatter')
#Calculating pearsons correlation between components
print(sp.pearsonr(IT_index.CompA, IT_index.CompB))
print(sp.pearsonr(IT_index.CompA, IT_index.CompC_norm))
print(sp.pearsonr(IT_index.CompB, IT_index.CompC_norm))


