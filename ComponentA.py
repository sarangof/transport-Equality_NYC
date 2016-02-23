import pylab as pl
import pandas as pd
import numpy as np
import scipy.stats
import statsmodels.api as sm
Income2013 = pd.read_csv('2013 income pc.csv',  header=True, names=["id", "id2block", "block", "PCincome", "error"]                         , usecols=["id2block", "PCincome"])
Income2013.PCincome = Income2013.PCincome.replace("-", "0")
Income2013.PCincome = Income2013.PCincome.astype(int)
Income2013.head()
Mtrans2013 = pd.read_csv('Mean of transportation.csv',  header=True, usecols=[1, 5, 21,37])
Mtrans2013.columns = ['id2block', 'Car', 'PTrans', 'Bike']
Mtrans2013.head()
Mtrans2013['Tcommuters'] = Mtrans2013.Car + Mtrans2013.PTrans + Mtrans2013.Bike
Mtrans2013['Pcar'] = Mtrans2013.Car/Mtrans2013.Tcommuters
Mtrans2013['PPTrans'] = Mtrans2013.PTrans/Mtrans2013.Tcommuters
Mtrans2013['PBike'] = Mtrans2013.Bike/Mtrans2013.Tcommuters
Costcar2013 = pd.read_excel('norteast CES 2013.xlsx',  header=True, usecols=["Item", "New York"])
Costcar2013 = Costcar2013[43:46]
Costcar2013
Carcost = sum(Costcar2013["New York"])
Carcost
Costptrans2013 = pd.read_excel('Public transportation costs.xlsx')
Costptrans2013
Costptrans2013['Pondcost'] = Costptrans2013.Porcentage*Costptrans2013['Value per trip']*Costptrans2013['Trips per year']
PTcost = sum(Costptrans2013.Pondcost)
PTcost
Bcost = 95
CompA = pd.merge(Income2013, Mtrans2013, on=['id2block'])
CompA.head()
CompA['CompA'] = np.log((CompA.Pcar*Carcost + CompA.PPTrans*PTcost + CompA.PBike*Bcost)/(CompA.PCincome))
CompA.head()
CompA.CompA.describe()