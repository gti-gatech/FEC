# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

"""
This module calculates energy consumption rates for given scenario and meteorological settings
by looking up the value from the Moves ER Table

This module covers up Excel worksheets OpModeSummary and InputOutputBus partially
"""
import data_reader as dr
import constants as c
#import math
#import pandas as pd
#import bin_processor
#import hybrid_processor
import op_mode_summary
import util
from HVAC_power_cons import get_hvac_power_cons


from pandas import read_csv



def get_energy_consumption_values(speeds, number_of_passengers, cycle_location,
                                  year, road_type_id, source_type_id, hours_in_operation,
                                  ambient_temperature_degree_f, relative_humidity, charging_requirement,
                                  all_electric_range_miles, route_length, fuel_type_id_ice,
                                  fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series, no_of_runs_per_day,
                                  power_train_architecture, fuel_type_id_be, fuel_type_id_fce, fuel_type_id_pfce,
                                  fuel_type_id_phe, city_name, idle_speed_range, fuel_type_id_ice_2,
                                  FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR):
    # Get the Moves Lookup table

    moves_df = read_csv("MovesER/"+"MovesER_{st:d}_{yr:d}.csv".format(st=source_type_id,yr=year), sep=',')

    # Get the cycle information
#    cycle_df = dr.fetch_data_table(c.CYCLE_LOOKUP_FILE)

#    speeds = cycle_df[cycle_name]   # [xiaodan]need modification after adding custimized traces
    count = len(speeds) - len(speeds[speeds.isnull()]) - 1
    dist = speeds.sum()/3600.0
    avg_speed = dist/count*3600.0
#    hours_in_operation = route_length/avg_speed

    # Decide the roughness index based on the city
    city_df = dr.fetch_data_table(c.CITY_LOOKUP_FILE)
    roughness_index = float(city_df[city_df["NAME"] == city_name]["ROUGHNESS INDEX"])
    #print "hello there"
    #print roughness_index
    binned_data_df, binned_data_df_parallel, binned_data_df_series = \
                                                        op_mode_summary.get_op_mode_summary(speeds, 
                                                                                            number_of_passengers, 
                                                                                            ambient_temperature_degree_f, 
                                                                                            relative_humidity,
                                                                                            roughness_index,
                                                                                            idle_speed_range,
                                                                                            FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR)
     
#    print(binned_data_df_series)
    def get_energy_consumption(fuel_type_id, binned_data_df):
        def lookup_value(bin_no):
            if bin_no == 1 or bin_no == 0:
                return int(str(cycle_location) + "0" + str(bin_no) + str(year) + str(fuel_type_id) + str(source_type_id))
            return int(str(cycle_location) + str(bin_no) + str(year) + str(fuel_type_id) + str(source_type_id))
        moves_dfi = moves_df.set_index('metbinyearfuelsource')
        binned_data_df['metbinyearfuelsource'] = binned_data_df.STPOMBin.map(lookup_value)
        binned_data_dfi = binned_data_df.set_index('metbinyearfuelsource')
        energy_consumption_dfs = binned_data_dfi.join(moves_dfi, lsuffix='_l')
        energy_consumption_dfs['EnergyConsumptionRate']  = energy_consumption_dfs['91'] * 3600.0 / c.KWH_TO_MMBTU
        energy_consumption_dfs['CycleEnergyConsumption'] = energy_consumption_dfs['EnergyConsumptionRate'] * energy_consumption_dfs.CycleBinCounts /3600.0
        energy_consumption_dfs['RouteEnergyConsumption'] = energy_consumption_dfs.EnergyConsumptionRate * hours_in_operation * energy_consumption_dfs.Fraction/100.0
        energy_sum = energy_consumption_dfs['RouteEnergyConsumption'].sum()
#        print energy_consumption_dfs
        return energy_sum, energy_consumption_dfs
    
    energy_sum_ice, energy_consumption_dfs_ice = get_energy_consumption(fuel_type_id_ice, binned_data_df)
#    util.df_to_csv_debug(energy_consumption_dfs_ice, "sici energy consumptions.csv")
    energy_sum_ice_2, energy_consumption_dfs_ice_2 = get_energy_consumption(fuel_type_id_ice_2, binned_data_df)
    energy_sum_series, energy_consumption_dfs_series = get_energy_consumption(fuel_type_id_hybrid_series, binned_data_df_series)
#    util.df_to_csv_debug(energy_consumption_dfs_series, "series energy consumptions.csv")
    energy_sum_parallel, energy_consumption_dfs_parallel = get_energy_consumption(fuel_type_id_hybrid_parallel, 
                                                                                  binned_data_df_parallel)
#    util.df_to_csv_debug(energy_consumption_dfs_parallel, "parallel energy consumptions.csv")
    
    # Energy sum  to be multiplied by 100 before returning
#    energy_sum_series  *= 100
#    energy_sum_parallel *= 100
#    print(binned_data_df_series)
    pos_cycle_observed_work_sum = binned_data_df_series.loc[binned_data_df_series['CycleObservedWork'] >= 0,'CycleObservedWork'].sum()
    neg_cycle_observed_work_sum = binned_data_df_series.loc[binned_data_df_series['CycleObservedWork'] < 0,'CycleObservedWork'].sum()
    AUX_E_LOAD_SERIES = get_hvac_power_cons(ambient_temperature_degree_f, relative_humidity)[0]

    total_entries = binned_data_df.CycleBinCounts.sum()
#    print(hours_in_operation, 1/avg_speed)
    energy_sum_battery_electric = pos_cycle_observed_work_sum * \
            hours_in_operation/(total_entries/3600) / c.INVERTER_EFFICIENCY/ c.MOTOR_EFFICIENCY / c.BATTERY_EFFICIENCY + \
            neg_cycle_observed_work_sum * c.REGEN_BRAKING_EFFICIENCY + \
            AUX_E_LOAD_SERIES * total_entries / 3600 / c.BATTERY_EFFICIENCY
    
    energy_sum_fuel_cell_electric = pos_cycle_observed_work_sum * \
        hours_in_operation/(total_entries/3600)/ c.MOTOR_EFFICIENCY/ c.FUEL_CELL_EFFICIENCY + \
            neg_cycle_observed_work_sum * c.REGEN_BRAKING_EFFICIENCY+ \
            AUX_E_LOAD_SERIES * total_entries / 3600 / c.FUEL_CELL_EFFICIENCY
    
    # Calculate energy consumption for Plug In Hybrid Vehicles
    if charging_requirement == c.END_OF_RUN:
        if all_electric_range_miles >= route_length:
            energy_sum_pfce = energy_sum_battery_electric
        else:
            energy_sum_pfce = all_electric_range_miles/route_length*energy_sum_battery_electric + \
                                          (1-all_electric_range_miles/route_length)*energy_sum_fuel_cell_electric
    else:
        if all_electric_range_miles >= no_of_runs_per_day * route_length:
            energy_sum_pfce = energy_sum_battery_electric
        else:
            energy_sum_pfce = all_electric_range_miles/(number_of_passengers*route_length)*energy_sum_battery_electric + \
                                          (1-all_electric_range_miles/route_length)*energy_sum_fuel_cell_electric
    
    if charging_requirement == c.END_OF_RUN:
        if all_electric_range_miles >= route_length:
            energy_sum_phe = energy_sum_battery_electric
        else:
            if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                energy_sum_phe = all_electric_range_miles/route_length*energy_sum_battery_electric + \
                (1-all_electric_range_miles/route_length)*energy_sum_parallel
            else:
                energy_sum_phe = all_electric_range_miles/route_length*energy_sum_battery_electric + \
                (1-all_electric_range_miles/route_length)*energy_sum_series
    else:
        if all_electric_range_miles >= no_of_runs_per_day*route_length:
            energy_sum_phe = energy_sum_battery_electric
        else:
            if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                energy_sum_phe = all_electric_range_miles/(no_of_runs_per_day * route_length)*energy_sum_battery_electric + \
                                            (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*energy_sum_parallel
            else:
                energy_sum_phe = all_electric_range_miles/(no_of_runs_per_day * route_length)*energy_sum_battery_electric + \
                (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*energy_sum_series

    energy_sum_dict = {
        1 : energy_sum_ice,
        2 : energy_sum_ice_2,
        3 : energy_sum_parallel,
        4 : energy_sum_series,
        5 : energy_sum_battery_electric,
        6 : energy_sum_fuel_cell_electric,
        7 : energy_sum_pfce,
        8 : energy_sum_phe
    }

    fuel_type_dict = {
        1 : fuel_type_id_ice,
        2 : fuel_type_id_ice_2,
        3 : fuel_type_id_hybrid_parallel,
        4 : fuel_type_id_hybrid_series,
        5 : fuel_type_id_be,                                  
        6 : fuel_type_id_fce,
        7 : fuel_type_id_pfce,
        8 : fuel_type_id_phe
    }
    
    energy_consumption_dfs_dict = {
        1 : energy_consumption_dfs_ice,
        2 : energy_consumption_dfs_ice_2,
        3 : energy_consumption_dfs_parallel,
        4 : energy_consumption_dfs_series,
        5 : energy_consumption_dfs_ice,
        6 : energy_consumption_dfs_ice,
        7 : energy_consumption_dfs_ice,
        8 : energy_consumption_dfs_ice
    }
#    print energy_sum_dict

    return energy_sum_dict, fuel_type_dict, energy_consumption_dfs_dict




