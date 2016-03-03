# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:38:29 2016

@author: saf537
"""

import shapefile as shp
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

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

"""
# Component B - time versus distance
"""

"""
# Component C - Accesibility
"""