# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#import energy_consumption
import emissions
import sys
import json


cycle_name, number_of_passengers, cycle_location,\
year, road_type_id, source_type_id, hours_in_operation,\
ambient_temperature_degree_f, relative_humidity, charging_requirement,\
all_electric_range_miles, route_length, fuel_type_id_ice,\
fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series, no_of_runs_per_day,\
power_train_architecture, fuel_type_id_be, fuel_type_id_fce, fuel_type_id_pfce,\
fuel_type_id_phe, number_of_runs_per_bus_per_year, number_of_buses, city = sys.argv[1:]

city = city.replace("_", ", ")
                                  
emissions_output_total, annual_total_emissions, energy_sum_dict = emissions.get_emissions(cycle_name, int(number_of_passengers), int(cycle_location), int(year), 
                                   int(road_type_id), int(source_type_id), float(hours_in_operation),
                                   float(ambient_temperature_degree_f), float(relative_humidity), charging_requirement, 
                                   float(all_electric_range_miles), float(route_length), int(fuel_type_id_ice), int(fuel_type_id_hybrid_parallel), 
                                   int(fuel_type_id_hybrid_series), int(no_of_runs_per_day), power_train_architecture, 
                                   int(fuel_type_id_be), int(fuel_type_id_fce), 
                                   int(fuel_type_id_pfce), int(fuel_type_id_phe), int(number_of_runs_per_bus_per_year), int(number_of_buses), city)

emissions_output_total_json = emissions_output_total.to_json()
annual_total_emissions_json = annual_total_emissions.to_json()


final_dict = { 
                "energy_values"          : energy_sum_dict,
                "emissions_output_total" : emissions_output_total_json,
                "annual_total_emissions" : annual_total_emissions_json
             }

data_string = json.dumps(final_dict)
print data_string

# <codecell>

# <codecell>


