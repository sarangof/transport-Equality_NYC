# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:38:29 2016

@author: saf537
"""

import shapefile as shp
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pylab as pl
import pandas as pd
import numpy as np
import scipy.stats
import statsmodels.api as sm
import glob
import requests
import io

# get data file names
dfs = []
for i in [0,1]:
    url = 'http://lehd.ces.census.gov/data/lodes/LODES7/ny/od/ny_od_main_JT0'+ str(i) +'_2013.csv.gz'
    s=requests.get(url).content
    c=pd.read_csv(io.StringIO(s.decode('utf-8')))
    dfs.append(c)
# Concatenate all data into one DataFrame

big_frame = pd.concat(dfs, ignore_index=True)

sf = shp.Reader("data/nycb2010.shp")

sf = shp.Reader("data/nycb2010.shp")

#map = Basemap(llcrnrlon=-0.5,llcrnrlat=39.8,urcrnrlon=4.,urcrnrlat=43.,
#             resolution='i', projection='tmerc', lat_0 = 39.5, lon_0 = 1)
#
#map.drawmapboundary(fill_color='aqua')
#map.fillcontinents(color='#ddaa66',lake_color='aqua')
#map.drawcoastlines()
#map.readshapefile("data/nycb2010.shp",'nycb2010')
#
#plt.show()



""" Initial step: build number of people that travel between block groups by mode.
"""

# Load number of people travelling between block groups.


# Load modes per people, transform to frequency

"""
Component A - transportation expenses versus income
"""

#
#Income2013 = pd.read_csv('data/2013income pc.csv',  header=True, names=["id", "id2block", "block", "PCincome", "error"] , usecols=["id2block", "PCincome"])
#Income2013.PCincome = Income2013.PCincome.replace("-", "0")
#Income2013.PCincome = Income2013.PCincome.astype(int)
#Mtrans2013 = pd.read_csv('data/Meanoftransportation.csv',  header=True, usecols=[1, 5, 21,37])
#Mtrans2013.columns = ['id2block', 'Car', 'PTrans', 'Bike']
#Mtrans2013['Tcommuters'] = Mtrans2013.Car + Mtrans2013.PTrans + Mtrans2013.Bike
#Mtrans2013['Pcar'] = Mtrans2013.Car/Mtrans2013.Tcommuters
#Mtrans2013['PPTrans'] = Mtrans2013.PTrans/Mtrans2013.Tcommuters
#Mtrans2013['PBike'] = Mtrans2013.Bike/Mtrans2013.Tcommuters
#Costcar2013 = pd.read_excel('data/norteastCES2013.xlsx',  header=True, usecols=["Item", "New York"])
#Costcar2013 = Costcar2013[43:46]
#Carcost = sum(Costcar2013["New York"])
#Costptrans2013 = pd.read_excel('data/Publictransportation costs.xlsx')
#Costptrans2013['Pondcost'] = Costptrans2013.Porcentage*Costptrans2013['Value per trip']*Costptrans2013['Trips per year']
#PTcost = sum(Costptrans2013.Pondcost)
#Bcost = 95
#CompA = pd.merge(Income2013, Mtrans2013, on=['id2block'])
#CompA = CompA[CompA.CompA < 1]
#CompA['CompA'] = np.log((CompA.Pcar*Carcost + CompA.PPTrans*PTcost + CompA.PBike*Bcost)/(CompA.PCincome))
#CompA['CompA1'] = (CompA.CompA - CompA.CompA.min())/(CompA.CompA.max() - CompA.CompA.min())
#


"""
# Component B - time versus distance
"""

"""
# Component C - Accesibility
"""