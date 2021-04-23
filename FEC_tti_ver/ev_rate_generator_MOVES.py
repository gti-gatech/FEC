# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:11:48 2019

@author: X-Xu
"""

from pandas import read_csv
import pandas as pd
import boto3
import itertools
import numpy as np




### calculator initializing, define env parameters ###
s3 = boto3.client('s3')
bucket = 'tempo-tti'
cycle_source = 'MOVES'

cycle_summary_df = read_csv('output/EV220_energy_rate.csv', sep = ',')

# <codecell>
### interpolate EV energy rates and post-process ####        
cycle_summary_df['speed_bin'] = np.round(cycle_summary_df['speed_bin'], 0)
cycle_summary_df['speed_bin'] = cycle_summary_df['speed_bin'].astype(int)
#energy_rate_df = pd.merge(input_data_df, cycle_summary_df, on = 'cycle_path')


existing_speed_bin = list(cycle_summary_df['speed_bin'].unique())
speed_bin_interp = list(range(min(existing_speed_bin), max(existing_speed_bin)+1, 1))

speed_bin_interp = list(set(speed_bin_interp) - set(existing_speed_bin))
existing_speed_bin = np.array(existing_speed_bin)
#print(speed_bin_interp)
out_emission_rate_df = cycle_summary_df[['veh_type', 'speed_bin', 'elec_rate(kWh/mile)']]
for s in speed_bin_interp:
    print('generating energy rates for speed bin ' + str(s))
    closest_speed_bin_pool = existing_speed_bin - s
    lower_bound = max(existing_speed_bin[closest_speed_bin_pool<0])
    upper_bound = min(existing_speed_bin[closest_speed_bin_pool>0])
    print(lower_bound, upper_bound)
    energy_rate_lower_bound = cycle_summary_df.loc[cycle_summary_df['speed_bin'] == lower_bound]
    energy_rate_upper_bound = cycle_summary_df.loc[cycle_summary_df['speed_bin'] == upper_bound]
    energy_rate_to_interp = pd.merge(energy_rate_lower_bound, energy_rate_upper_bound, on = ['veh_type'], how = 'inner')
    print(len(energy_rate_lower_bound), len(energy_rate_upper_bound))
### applyMOVES magic formula, EFInterp = EFLowSpeed - FACInterp * (EFLowSpeed - EFHighSpeed) #### 
    FACInterp = (1.0/s - 1.0/lower_bound) / (1.0/upper_bound - 1.0/lower_bound)
    energy_rate_to_interp['elec_rate(kWh/mile)'] = energy_rate_to_interp['elec_rate(kWh/mile)_x'] - FACInterp * (energy_rate_to_interp['elec_rate(kWh/mile)_x'] - energy_rate_to_interp['elec_rate(kWh/mile)_y'])
    energy_rate_to_interp['speed_bin'] = s
    out_energy_rate_interp = energy_rate_to_interp[['veh_type', 'speed_bin', 'elec_rate(kWh/mile)']]
    out_emission_rate_df = pd.concat([out_emission_rate_df, out_energy_rate_interp])
#    break
    
# <codecell>
low_speed_to_fill = list(range(2, min(existing_speed_bin)))
high_speed_to_fill = list(range(max(existing_speed_bin)+1, 81))

for v in low_speed_to_fill:
    energy_rate_to_fill = out_emission_rate_df.loc[out_emission_rate_df['speed_bin'] == min(existing_speed_bin)]
    energy_rate_to_fill.loc[:, 'speed_bin'] = v
    out_emission_rate_df = pd.concat([out_emission_rate_df, energy_rate_to_fill])


for v in high_speed_to_fill:
    energy_rate_to_fill = out_emission_rate_df.loc[out_emission_rate_df['speed_bin'] == max(existing_speed_bin)]
    energy_rate_to_fill.loc[:, 'speed_bin'] = v
    out_emission_rate_df = pd.concat([out_emission_rate_df, energy_rate_to_fill])  
    
#out_emission_rate_df['elec_rate_from_grid(kJ/mile)'] = out_emission_rate_df['elec_rate(kJ/mile)'] / charging_eff / transmission_eff
#out_emission_rate_df = out_emission_rate_df.drop_duplicates(subset=['veh_type', 'speed_bin', 'HVAC_load', 'initial_soc', 'road_grade'], keep='first')


# <codecell>
file_name = 'BET52_rates_from_' + cycle_source + '.csv'
out_path = 's3://' + '/'.join((bucket, 'EV-Matrix', 'EV_rates', file_name))
out_emission_rate_df.to_csv(out_path, sep = ',', index = False)
out_emission_rate_df.to_csv(file_name, sep = ',', index = False)
    
