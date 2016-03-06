# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:38:29 2016

@author: saf537
"""

#import shapefile as shp
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import pylab as pl
import pandas as pd
import numpy as np

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

CompA.set_index(CompA['id2block'])
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


timeW['CompB']    = timeW['av_time']/1
timeW=timeW.rename(columns = {'Id2':'id2block'})
IT_index = pd.merge(timeW[['id2block','CompB']],CompA[['id2block','CompA']],on = 'id2block')



"""
# Component C - Accesibility
"""

C3 = pd.read_table('data/CB_final.txt', sep = ',',usecols=['BCTCB2010','Area', 'Within_Met', 'Num_Bus_Stop','Within_Buf'])
C3=C3.rename(columns = {'BCTCB2010':'id2block'})
IT_index['id2block'] = IT_index['id2block'].astype(str).str[1:].astype(np.int64)

C3['CompC'] = C3['Within_Buf'] / C3['Area']

#IT_index = pd.merge(C3[['id2block','CompC']],IT_index,on='id2block')

#IT_index['CompC'] = 1
