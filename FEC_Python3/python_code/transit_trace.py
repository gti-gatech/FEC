# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:51:12 2015

@author: arielxxd
"""

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
from os import listdir
import os
import util

print "this is the code Xiaodan made to transform website input into python input"





# below are user input
city = "Minneapolis--St. Paul_MN"
season = "Summer"
severity = 4
year = 2012
cycle_name= "Custom Input"
source_type_id = 42
route_length = 0
number_of_passengers = 0
number_of_runs_per_bus_per_year = 3650
number_of_buses = 500
no_of_runs_per_day = 10
idle_speed_range=1.0  #mph
fuel_type_id_ice = 2
fuel_type_id_ice_2 = 3
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
#parameter_set={}

for nvalue in range(len(source_type_physics)):
    if source_type_physics.ix[nvalue].sourceTypeID == source_type_id:
        if source_type_physics.ix[nvalue].beginModelYearID <= year and source_type_physics.ix[nvalue].endModelYearID >= year:
            FORMULA_B1 = source_type_physics.ix[nvalue].rollingTermA/source_type_physics.ix[nvalue].fixedMassFactor
            FORMULA_B2 = source_type_physics.ix[nvalue].rotatingTermB/source_type_physics.ix[nvalue].fixedMassFactor
            FORMULA_B3 = source_type_physics.ix[nvalue].dragTermC/source_type_physics.ix[nvalue].fixedMassFactor
            SOURCE_MASS_METRIC_TONNES = source_type_physics.ix[nvalue].sourceMass
            FIXED_MASS_FACTOR = source_type_physics.ix[nvalue].fixedMassFactor
#            print FORMULA_B1
#            print FORMULA_B2
#            print FORMULA_B3
#            print SOURCE_MASS_METRIC_TONNES
#            print FIXED_MASS_FACTOR
# 



#calculate cycle_location (meteorlogy number), temperature and humidity
meteotable = read_csv("MeteoLookup" + ".csv", sep=',')
#print meteotable
cycle_location = int(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Cycle Location"])
#print cycle_location
ambient_temperature_degree_f = float(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Temperature"])
#print ambient_temperature_degree_f
relative_humidity = float(meteotable[(meteotable["Season"] == season) & (meteotable["Severity"] == severity)]["Humidity"])
#print relative_humidity
#Edit customized input

alltrace=listdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code\\speed_xiaodan")
output_energy=pd.DataFrame(columns=('filename', 'energy_consumption (kwh)'),index=range(len(alltrace)))
print output_energy
i=0
#print output_energy
for f in alltrace:
    print(f)
    os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code")
    custom_input = read_csv("speed_xiaodan/"+ f, sep=',')
    cycle_df = dr.fetch_data_table(c.RAW_CYCLE_LOOKUP_FILE)
    custom_input.columns=[cycle_name]   
    full_cycle=pd.concat([cycle_df, custom_input], axis=1)
    full_cycle.to_csv(c.CYCLE_LOOKUP_FILE+".csv", sep='\t', encoding='utf-8')
#calculate hours_in_operation
    cycletable=read_csv("CycleLookup"+ ".csv",sep='\t')
    speeds = cycletable[cycle_name]
    route_length = speeds.sum()/3600.0
#print speeds
    count = len(speeds) - len(speeds[speeds.isnull()]) - 1
    dist = speeds.sum()/3600.0
    avg_speed = dist/count*3600.0
    hours_in_operation = route_length/avg_speed
#print hours_in_operation
#print cycletable
#print hours_in_operation

# same as python gateway, fetch the emission results. Need to solve the format issue
    city = city.replace("_", ", ")
#print city

    if idle_speed_range>=25:
        print "Idle speed range out of bound"
#    os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code")                                  
    emissions_output_total, annual_total_emissions, energy_sum_dict = emissions.get_emissions(cycle_name, int(number_of_passengers), int(cycle_location), int(year), 
                                   int(road_type_id), int(source_type_id), float(hours_in_operation),
                                   float(ambient_temperature_degree_f), float(relative_humidity), charging_requirement, 
                                   float(all_electric_range_miles), float(route_length), int(fuel_type_id_ice), int(fuel_type_id_hybrid_parallel), 
                                   int(fuel_type_id_hybrid_series), int(no_of_runs_per_day), power_train_architecture, 
                                   int(fuel_type_id_be), int(fuel_type_id_fce), 
                                   int(fuel_type_id_pfce), int(fuel_type_id_phe), int(number_of_runs_per_bus_per_year), int(number_of_buses), city, float(idle_speed_range),int(fuel_type_id_ice_2),
                                   float(FORMULA_B1),float(FORMULA_B2),float(FORMULA_B3),float(SOURCE_MASS_METRIC_TONNES),float(FIXED_MASS_FACTOR))

#    emissions_output_total_json = emissions_output_total.to_json()
#    annual_total_emissions_json = annual_total_emissions.to_json()
#
#
#    final_dict = { 
#                    "energy_values"          : energy_sum_dict,
#                    "emissions_output_total" : emissions_output_total_json,
#                    "annual_total_emissions" : annual_total_emissions_json
#                }
##print final_dict
#    data_string = json.dumps(final_dict)
#
#    df=pd.DataFrame([data_string])
#    temp=pd.Series([f,energy_sum_dict[3]])
#    output_energy.append(temp,ignore_index=True)
    output_energy['filename'].loc[i]=f
    output_energy['energy_consumption (kwh)'].loc[i]=energy_sum_dict[3]
    print output_energy
    i+=1

    
os.chdir("F:\\Study at GT\\Fuel Emission Calculator\\p1.ag\\python_code\\speed_xiaodan")
util.df_to_csv_debug(output_energy,"transit_result.csv")
#df.to_csv('emission_result.csv',sep='\t')
#print data_string
