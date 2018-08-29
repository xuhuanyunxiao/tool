# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:53:00 2018

@author: Administrator
"""


#%%
import numpy as np
import pandas as pd

from quilt.data.ResidentMario import missingno_data
import missingno as msno

#%% 数据
collisions = missingno_data.nyc_collision_factors()
collisions = collisions.replace("nan", np.nan)

#%%  Matrix
msno.matrix(collisions.sample(250))
#msno.matrix(busines_change)

#% 时间序列
null_pattern = (np.random.random(1000).reshape((50, 20)) > 0.5).astype(bool)
null_pattern = pd.DataFrame(null_pattern).replace({False: None})
msno.matrix(null_pattern.set_index(pd.period_range('1/1/2011', '2/1/2015', freq='M')) , freq='BQ')

#%% Bar Chart
msno.bar(collisions.sample(1000))

#%%  Heatmap
msno.heatmap(collisions)

#%% Dendrogram
msno.dendrogram(collisions)

#%%  Geoplot
msno.geoplot(collisions, x='LONGITUDE', y='LATITUDE')

#%%












