# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:58:54 2016

@author: saf537
"""

import pandas as pd
import urllib2
from StringIO import StringIO
import gzip
import numpy as np

Income2013 = pd.read_csv('data/2013Incomepc.csv',  header=1, names=["id", "id2block", "block", "PCincome", "error"] , usecols=["id2block", "PCincome"])

# get data file names
dfs = []
for i in [0,1]:
    baseURL = 'http://lehd.ces.census.gov/data/lodes/LODES7/ny/od/'
    filename = 'ny_od_main_JT0'+ str(i) +'_2013.csv.gz'
    response = urllib2.urlopen(baseURL + filename)
    compressedFile = StringIO()
    compressedFile.write(response.read())
    compressedFile.seek(0)
    decompressedFile = gzip.GzipFile(fileobj=compressedFile,mode='rb')
    data = pd.read_csv(decompressedFile,usecols=['w_geocode','h_geocode','S000']) 
    data['id2block'] = data['w_geocode'].astype(str).str[:-3].astype(np.int64)
    print(len(data))
    df = pd.merge(data,Income2013, on = ['id2block'],how='inner')
    print len(df)
    df['id2block'] = data['h_geocode'].astype(str).str[:-3].astype(np.int64)
    df = pd.merge(df,Income2013, on = ['id2block'],how='inner')
    print(len(df))