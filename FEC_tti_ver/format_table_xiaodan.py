# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 15:59:43 2015

@author: arielxxd
"""

import pandas as pd
from pandas import read_csv
cycletable = read_csv("CycleLookup0" + ".csv", sep=',')
print cycletable

df=pd.DataFrame([cycletable])
df.to_csv('CycleLookup.csv',sep='\t')

