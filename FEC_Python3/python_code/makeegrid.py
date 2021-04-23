# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:34:07 2015

@author: arielxxd
"""
#import data_reader as dr
from pandas import read_csv
import pandas as pd

custom_input = read_csv("egrid.csv", sep=',')
#cycle_df = dr.fetch_data_table(c.RAW_CYCLE_LOOKUP_FILE)
    #full_cycle=pd.concat([cycle_df, custom_input], axis=1)
egrid=pd.DataFrame(custom_input)
egrid.to_csv("eGridLookup.csv", sep='\t', encoding='utf-8')