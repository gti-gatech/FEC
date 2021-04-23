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
import warnings
from os import listdir

print("this is the code Xiaodan made to transform website input into python input")



def main():
    BET_results = []
    warnings.simplefilter('always')
    # below are user input
    city = "Houston_TX"
    season = "Summer"
    severity = 4
    year = 2020
    cycle_name= "Custom Input"
    source_type_id = 52
    route_length = 1
    number_of_passengers = 0
    number_of_runs_per_bus_per_year = 3650
    number_of_buses = 500
    no_of_runs_per_day = 1
    idle_speed_range=1.0  #mph
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
    
    
    #Edit customized input
    alltrace=listdir("cycle")
    meteotable = read_csv("MeteoLookup" + ".csv", sep=',')
    #print meteotable
    cycle_location = int(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Cycle Location"])
    #print cycle_location
    ambient_temperature_degree_f = float(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Temperature"])
    #print ambient_temperature_degree_f
    relative_humidity = float(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Humidity"])
    #print relative_humidity
    #output_energy=pd.DataFrame(columns=('filename', 'energy_consumption (kwh)'),index=range(len(alltrace)))
    #print output_energy
    i = 0
    #print output_energy
    global trip_name
    for f in alltrace:
        if f == '.DS_Store':
            continue
        trip_name = f.split('.csv')[0]
        print(trip_name)
    #    os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code")
        custom_input = read_csv("cycle/"+ f, sep=',')
        cycle_df = dr.fetch_data_table(c.RAW_CYCLE_LOOKUP_FILE)
        custom_input.columns=[cycle_name]   
        full_cycle=pd.concat([cycle_df, custom_input], axis=1)
        full_cycle.to_csv(c.CYCLE_LOOKUP_FILE+".csv", sep='\t', encoding='utf-8')
    #calculate hours_in_operation
        cycletable=read_csv("CycleLookup"+ ".csv",sep='\t')
        speeds = cycletable[cycle_name]
#        route_length = speeds.sum()/3600.0
    #print speeds
        count = len(speeds) - len(speeds[speeds.isnull()]) - 1
        dist = speeds.sum()/3600.0
        avg_speed = dist/count*3600.0
        print(avg_speed)
        hours_in_operation = dist/avg_speed
    #print hours_in_operation
    #print cycletable
    #print hours_in_operation
    
    # same as python gateway, fetch the emission results. Need to solve the format issue
        city = city.replace("_", ", ")
    #print city
    
        if idle_speed_range>=25:
            print("Idle speed range out of bound")
    #    os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code")                                  
        #Run FEC model	
        fuel_upstream_df, fuel_tailpipe_df, emissions_output_total, annual_total_emissions, energy_sum_dict = emissions.get_emissions(cycle_name, int(number_of_passengers), int(cycle_location), int(year), 
                                           int(road_type_id), int(source_type_id), float(hours_in_operation),
                                           float(ambient_temperature_degree_f), float(relative_humidity), charging_requirement, 
                                           float(all_electric_range_miles), float(route_length), int(fuel_type_id_ice), int(fuel_type_id_hybrid_parallel), 
                                           int(fuel_type_id_hybrid_series), int(no_of_runs_per_day), power_train_architecture, 
                                           int(fuel_type_id_be), int(fuel_type_id_fce), 
                                           int(fuel_type_id_pfce), int(fuel_type_id_phe), int(number_of_runs_per_bus_per_year), int(number_of_buses), city, float(idle_speed_range),int(fuel_type_id_ice_2),
                                           float(FORMULA_B1),float(FORMULA_B2),float(FORMULA_B3),float(SOURCE_MASS_METRIC_TONNES),float(FIXED_MASS_FACTOR))
    
    
        i+=1
        print(energy_sum_dict[5])
        BET_results.append([trip_name, source_type_id, avg_speed, energy_sum_dict[5]])
    BET_results_df = pd.DataFrame(BET_results, columns =['cycle', 'veh_type', 'speed_bin', 'elec_rate(kWh/mile)']) 
    print(BET_results_df)
#        BET_results_df.to_csv('output/EV220_energy_rate.csv')
#os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code\\speed_xiaodan")
#util.df_to_csv_debug(output_energy,"transit_result.csv")

main()