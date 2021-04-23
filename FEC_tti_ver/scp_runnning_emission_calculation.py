# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import data_reader as dr
import constants as c
import pandas as pd
from pandas import read_csv


def get_pollutant_emissions(year, road_type_id, source_type_id, fuel_type_ids, 
                            cycle_location, technology_ids, hours_in_operation,
                            energy_consumption_dfs_dict):
    
    # Get the Moves Lookup table
    moves_df = read_csv("MovesER/"+"MovesER_{st:d}_{yr:d}.csv".format(st=source_type_id,yr=year), sep=',')
    moves_df = moves_df.set_index('metbinyearfuelsource')

    # Get the Pollutants name to id map
    pollutants_df = dr.fetch_data_table(c.POLLUTANTS_FILE)
    # Remove the pollutant ID 111 since we do not have the corresponding moves information for it and it shall not be required
    pollutants_df = pollutants_df[pollutants_df.pollutantID != 111]
    bins = moves_df.opModeBin.unique()
    bins_df = pd.DataFrame({'Key' : 1, 'BinNo' : bins})
    pollutants_dummy_df = pollutants_df.copy()
    pollutants_dummy_df['Key']  = 1
    moves_emissions_results_df = pd.merge(pollutants_dummy_df, bins_df, on='Key')
    del(moves_emissions_results_df['Key'])
    temp_results = {}
    results_final = {}
    for index, tech_id in enumerate(technology_ids):
        if tech_id not in (3, 6, 7, 5):
#            technology_id = technology_ids[index]
            fuel_type_id = fuel_type_ids[index+1]
            def lookup_value(bin_no):
                if bin_no == 1 or bin_no == 0:
                    return int(str(cycle_location) + "0" + str(bin_no) + str(year) + str(fuel_type_id) + str(source_type_id))
                return int(str(cycle_location) + str(bin_no) + str(year) + str(fuel_type_id) + str(source_type_id))
            temp_results[index+1] = moves_emissions_results_df.copy()
            temp_results[index+1]['metbinyearfuelsource'] = temp_results[index+1].BinNo.map(lookup_value)
            grouped = temp_results[index+1].groupby(['pollutantID'])
            def get_emissions(grouped):
                grouped2 = grouped.copy().set_index('metbinyearfuelsource')
                merged =  grouped2.join(moves_df, how='left', lsuffix='_l')
                pollutantId = grouped.pollutantID.unique()[0]
#                print pollutantId
                return merged[str(pollutantId)] * 3600 * hours_in_operation * energy_consumption_dfs_dict[index+1].Fraction/100
            results_final[index+1] = grouped.apply(get_emissions)
            results_final[index+1] = results_final[index+1].transpose()

    return results_final




