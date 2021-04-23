# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pandas import read_csv
import emissions
#import sys
import json
import pandas as pd
import data_reader as dr
import constants as c
#import warnings
from os import listdir
import os
import bin_processor as bp
import data_reader as dr
import constants as c
#from HVAC_power_cons import get_hvac_power_cons

print("this is the code Xiaodan made to transform website input into python input")



def main():
#    BET_results = []
#    warnings.simplefilter('always')
    # below are user input\
    min_idling_for_charging = 600 # need at least 600 s for charging events
    city = "Houston_TX"
    season = "Summer"
    severity = 2
    year = 2018
    cycle_name= "Custom Input"
    source_type_id = 61
    route_length = 1
    max_load = 80000
    number_of_runs_per_bus_per_year = 3650
    number_of_buses = 500
    no_of_runs_per_day = 1
    idle_speed_range=3.0  #mph
    fuel_type_id_ice = 2
    fuel_type_id_ice_2 = 210
    fuel_type_id_hybrid_parallel = 2
    fuel_type_id_hybrid_series = 2
    fuel_type_id_be = 2
    fuel_type_id_fce = 0
    fuel_type_id_pfce = 0
    fuel_type_id_phe = 2
    # below are default input
    road_type_id = 5
    charging_requirement = "End_of_Run"
    all_electric_range_miles = 5
    power_train_architecture = "Series"
    
    
    #below are values need to be calculated
    cycle_location = 0
    hours_in_operation = 0
    ambient_temperature_degree_f = 0
    relative_humidity = 0
    
    FORMULA_B1 = 0
    FORMULA_B2 = 0
    FORMULA_B3 = 0
    SOURCE_MASS_METRIC_TONNES = 0
    FIXED_MASS_FACTOR = 0
    
    source_type_physics = read_csv(c.SOURCE_TYPE_PHYSICS + ".csv", sep=',')
    
    # take parameters from source type physics table
    for nvalue in range(len(source_type_physics)):
        if source_type_physics.loc[nvalue].sourceTypeID == source_type_id:
            if source_type_physics.loc[nvalue].beginModelYearID <= year and source_type_physics.loc[nvalue].endModelYearID >= year:
                FORMULA_B1 = source_type_physics.loc[nvalue].rollingTermA/source_type_physics.loc[nvalue].fixedMassFactor
                FORMULA_B2 = source_type_physics.loc[nvalue].rotatingTermB/source_type_physics.loc[nvalue].fixedMassFactor
                FORMULA_B3 = source_type_physics.loc[nvalue].dragTermC/source_type_physics.loc[nvalue].fixedMassFactor
                SOURCE_MASS_METRIC_TONNES = source_type_physics.loc[nvalue].sourceMass
                FIXED_MASS_FACTOR = source_type_physics.loc[nvalue].fixedMassFactor
    #get meteorology
    if (max_load *c.POUNDS_TO_METRIC_TONS) <= SOURCE_MASS_METRIC_TONNES:
        number_of_passengers = 0
    else:
        number_of_passengers = (max_load - SOURCE_MASS_METRIC_TONNES/c.POUNDS_TO_METRIC_TONS)/c.PER_PASSENEGER_AVERAGE_WEIGHT
    print(number_of_passengers)
    meteotable = read_csv("MeteoLookup" + ".csv", sep=',')
    #print meteotable
    cycle_location = int(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Cycle Location"])
    #print cycle_location
    ambient_temperature_degree_f = float(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Temperature"])
    #print ambient_temperature_degree_f
    relative_humidity = float(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Humidity"])
#    AUX_E_LOAD_SERIES = get_hvac_power_cons(ambient_temperature_degree_f, relative_humidity)[0]

    #get raw cycle lookup table
    cycle_df = dr.fetch_data_table(c.RAW_CYCLE_LOOKUP_FILE)
    # same as python gateway, fetch the emission results. Need to solve the format issue
    city = city.replace("_", ", ")    
    
    # Decide the roughness index based on the city
    city_df = dr.fetch_data_table(c.CITY_LOOKUP_FILE)
    roughness_index = float(city_df[city_df["NAME"] == city]["ROUGHNESS INDEX"])
#    print('rough index is ' + str(roughness_index))

    if idle_speed_range>=25:
        print("Idle speed range out of bound")    
        
    #Edit customized input
    os.chdir('C:/Users/X-Xu/Documents/Energy foundation/608351 - HGAC - Drayage Truck Data/Data')
    inp_dir = "out_vehicle_trip"
    out_dir = "out_trip_energy"
    trip_dir = "out_vehicle_trip_split"
    allveh = listdir(inp_dir)
    


    i = 0
    #print output_energy
#    global trip_name
    output_attributes = ['veh', 'tripID', 'seqID', 'route_length', 'hours_in_operation', 
                         'idling_indicator','start_time', 'end_time',
                         'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude',
                         'ICEV_energy(kWh)', 'BEV_energy(kWh)']
    processed_list = ['HGAC_CENTRAL_1500042D']
#    , 'HGAC_CENTRAL_1503022C',
#                      'HGAC_CENTRAL_1503132C', 'HGAC_CENTRAL_1600942D',
#                      'HGAC_CENTRAL_1600952D', 'HGAC_CENTRAL_1600992D',
#                      'HGAC_CENTRAL_1603652C', 'HGAC_CENTRAL_1603892C',
#                      'HGAC_CLARK_72', 'HGAC_CLARK_74', 'HGAC_CLARK_78',
#                      'HGAC_CLARK_80'] 
#
#                      , 
#                      'HGAC_CLARK_80', 'HGAC_CLARK_93', 'HGAC_COALCITY_002']
    output_attributes.extend(c.GHG_EMISSIONS)
    for veh in allveh:
        if veh in processed_list:
            continue
        veh_results = []
        all_traces = listdir(inp_dir + '/' + veh)
        for f in all_traces:
            trip = read_csv(inp_dir + '/' + veh + '/' + f)
            trip_name = f.split('.csv')[0]
            print(trip_name)
        #    os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code")
#            custom_input = read_csv("cycle/"+ f, sep=',')
    #        cycle_df = dr.fetch_data_table(c.RAW_CYCLE_LOOKUP_FILE)
    #        custom_input.columns=[cycle_name]   
    #        full_cycle=pd.concat([cycle_df, custom_input], axis=1)
    #        full_cycle.to_csv(c.CYCLE_LOOKUP_FILE+".csv", sep='\t', encoding='utf-8')
    #    #calculate hours_in_operation
    #        cycletable=read_csv("CycleLookup"+ ".csv",sep='\t')
    #        speeds = cycletable[cycle_name]
            custom_input = trip['speed_filtered']
            speeds = custom_input
            speeds = speeds.rename(cycle_name)
#            print(speeds)
    
            #print speeds
#            count = len(speeds) - len(speeds[speeds.isnull()]) - 1
#            dist = speeds.sum()/3600.0
#            avg_speed = dist/count*3600.0
#            hours_in_operation = dist/avg_speed
    
            binned_data_df, bins, data_table = bp.get_binned_data(speeds, number_of_passengers, roughness_index, 
                                                                  idle_speed_range, FORMULA_B1,FORMULA_B2,FORMULA_B3,
                                                                  SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR)
            trip_with_bins = pd.concat([trip, data_table], axis=1)
            trip_with_bins.loc[:, 'idle_count'] = 0
            trip_with_bins.loc[:, 'idle_flag'] = 0
#            trip_with_bins.loc[:, 'idle_duration'] = 0
            len_trip = len(trip_with_bins)
            for index, row in trip_with_bins.iterrows():
                if (row['BinNo'] == 1 and index==0):
                    trip_with_bins.loc[index, 'idle_count'] = 1 
                elif (row['BinNo'] == 1 and index>0):
                    trip_with_bins.loc[index, 'idle_count'] = trip_with_bins.loc[index-1, 'idle_count'] + 1
                else:
                    trip_with_bins.loc[index, 'idle_count'] = 0
                    if (index > 0 and trip_with_bins.loc[index-1, 'idle_count']>=min_idling_for_charging):
                        trip_with_bins.loc[index, 'idle_flag'] = 1
#                        trip_with_bins.loc[index, 'idle_duration'] = trip_with_bins.loc[index-1, 'idle_count']
                        duration = trip_with_bins.loc[index-1, 'idle_count']
                        trip_with_bins.loc[index-duration, 'idle_flag'] = 1
                if (index == len_trip - 1 and trip_with_bins.loc[index, 'idle_count'] >= min_idling_for_charging):
                        duration = trip_with_bins.loc[index-1, 'idle_count']
                        trip_with_bins.loc[index-duration, 'idle_flag'] = 1
                                       
            trip_with_bins['trip_seq'] = trip_with_bins.loc[:, 'idle_flag'].cumsum()
            unique_seq = trip_with_bins['trip_seq'].unique()
            for seq in unique_seq:
                idling_indicator = 0
                trip_seq = trip_with_bins.loc[trip_with_bins['trip_seq'] == seq]
                if not os.path.isdir(trip_dir + '/' + veh):
                    os.mkdir(trip_dir + '/' + veh)
                trip_seq.to_csv(trip_dir + '/' + veh + '/' + trip_name + '-' + str(seq) +'.csv', index= False)
                if len(trip_seq) <= 1:
                    print('this trip has short seq')
                    continue
                if trip_seq['idle_count'].max() >= min_idling_for_charging:
                    idling_indicator = 1
                speeds = trip_seq['speed_filtered']
                speeds = speeds.rename(cycle_name)
                route_length = trip_seq['speed_filtered'].sum() / 3600.0
                hours_in_operation = len(trip_seq) / 3600.0
                start_time = trip_seq.head(1)['datetime'].values[0]
                end_time = trip_seq.tail(1)['datetime'].values[0]
                start_latitude = float(trip_seq.head(1)['Latitude'])	
                start_longitude = float(trip_seq.head(1)['Longitude'])		
                end_latitude = float(trip_seq.tail(1)['Latitude'])	
                end_longitude = float(trip_seq.tail(1)['Longitude'])	
                operation_result = [veh, trip_name, seq, route_length, hours_in_operation, 
                                    idling_indicator, start_time, end_time,
                                    start_latitude, start_longitude, end_latitude, end_longitude]

                os.chdir('C:/Users/X-Xu/Documents/TEMPO-Suite/EV_analysis/EV-analysis/FEC')
                full_cycle=pd.concat([cycle_df, speeds], axis=1)
                speeds = full_cycle[cycle_name]
#                full_cycle.to_csv(c.CYCLE_LOOKUP_FILE+".csv", sep='\t', encoding='utf-8')

#            trip_with_bins.to_csv('debug/' + 'test_idling.csv')
#                print(route_length, hours_in_operation)
           
                #Run FEC model	
                fuel_upstream_df, fuel_tailpipe_df, emissions_output_total, annual_total_emissions, energy_sum_dict = emissions.get_emissions(speeds, int(number_of_passengers), int(cycle_location), int(year), 
                                                   int(road_type_id), int(source_type_id), float(hours_in_operation),
                                                   float(ambient_temperature_degree_f), float(relative_humidity), charging_requirement, 
                                                   float(all_electric_range_miles), float(route_length), int(fuel_type_id_ice), int(fuel_type_id_hybrid_parallel), 
                                                   int(fuel_type_id_hybrid_series), int(no_of_runs_per_day), power_train_architecture, 
                                                   int(fuel_type_id_be), int(fuel_type_id_fce), 
                                                   int(fuel_type_id_pfce), int(fuel_type_id_phe), int(number_of_runs_per_bus_per_year), int(number_of_buses), city, float(idle_speed_range),int(fuel_type_id_ice_2),
                                                   float(FORMULA_B1),float(FORMULA_B2),float(FORMULA_B3),float(SOURCE_MASS_METRIC_TONNES),float(FIXED_MASS_FACTOR))
#                print(energy_sum_dict)
#                print(fuel_tailpipe_df)
                energy_result = [energy_sum_dict[1], energy_sum_dict[5]]
                emission_result = fuel_tailpipe_df[1].tolist()
                operation_result.extend(energy_result)
                operation_result.extend(emission_result)
                veh_results.append(operation_result)
#                print(operation_result)
                os.chdir('C:/Users/X-Xu/Documents/Energy foundation/608351 - HGAC - Drayage Truck Data/Data')
        
        
            i+=1
#            if i>10:
#                break
#            break
#        print(veh_results)
        veh_results_df = pd.DataFrame(veh_results, columns = output_attributes) 
        print(veh_results_df.head(10))
        veh_results_df.to_csv(out_dir + '/' + veh + '_energy.csv', sep=',', index = False)
#        break


main()