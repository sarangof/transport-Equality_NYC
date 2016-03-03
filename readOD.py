# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:58:54 2016

@author: saf537
"""

import shapefile as shp
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#import geopandas as gdp
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
for i in [0,5]:
    url = 'http://lehd.ces.census.gov/data/lodes/LODES7/ny/od/ny_od_main_JT0'+ str(i) +'_2013.csv.gz'
    s=requests.get(url).content
    c=pd.read_csv(io.StringIO(s.decode('utf-8')))
    dfs.append(c)
# Concatenate all data into one DataFrame

big_frame = pd.concat(dfs, ignore_index=True)

sf = shp.Reader("data/nycb2010.shp")
#