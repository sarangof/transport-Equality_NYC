# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:58:54 2016

@author: saf537
"""

import pandas as pd
import urllib2
from StringIO import StringIO
import gzip

# get data file names
dfs = []
for i in [0,1]:
    baseURL = 'http://lehd.ces.census.gov/data/lodes/LODES7/ny/od/'
    filename = 'ny_od_main_JT0'+ str(i) +'_2013.csv.gz'
    outFilePath = filename[:-3]    
    response = urllib2.urlopen(baseURL + filename)
    compressedFile = StringIO(response.read())
    decompressedFile = gzip.GzipFile(fileobj=compressedFile) 
    with open(outFilePath,'w') as outfile:
        outfile.write(decompressedFile.read())
    df = pd.read_csv(outFilePath)
    df.drop(df.columns[2:],axis=1)
print df.head()    
