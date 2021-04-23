# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Imports
import constants as c
import pandas as pd
import data_reader as dr
import energy_consumption
import scp_runnning_emission_calculation as scprec
import util



def get_emissions(speeds, number_of_passengers, cycle_location, year, road_type_id, source_type_id, hours_in_operation,
                  ambient_temperature_degree_f, relative_humidity, charging_requirement, all_electric_range_miles,
                  route_length, fuel_type_id_ice, fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series,
                  no_of_runs_per_day, power_train_architecture, fuel_type_id_be, fuel_type_id_fce, 
                  fuel_type_id_pfce, fuel_type_id_phe, number_of_runs_per_bus_per_year, number_of_buses, city_name, idle_speed_range,fuel_type_id_ice_2,
                  FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR):
    
#    cycle_df = dr.fetch_data_table(c.CYCLE_LOOKUP_FILE)
    city_df = dr.fetch_data_table(c.CITY_LOOKUP_FILE)
    state = city_df[city_df["NAME"] == city_name]["State"]
#    print state

#    speeds = cycle_df[cycle_name]
    count = len(speeds) - len(speeds[speeds.isnull()]) - 1
    dist = speeds.sum()/3600.0
    avg_speed = dist/count*3600.0
#    hours_in_operation = route_length/avg_speed
    #print "Hours in operation in EC ", hours_in_operation
    
    # Get the Moves Lookup table
#    moves_df = dr.fetch_data_table(c.MOVES_ER_FILE)
    
    # Get the Greet Lookup table
#    global greet_df
    greet_df = dr.fetch_data_table(c.GREET_LOOKUP_FILE)
    greet_df.set_index("Fuelyear", inplace=True)
#    print greet_df.head(10)
    
    egrid_df = dr.fetch_data_table(c.EGRID_LOOKUP_FILE)
    egrid_df.set_index("State",inplace=True)
#    print egrid_df

    # Get the fuel name map
    fuel_id_name_map_df = dr.fetch_data_table(c.FUEL_TYPE_ID_NAME_MAP_FILE)
    fuel_id_name_map_df.set_index("FuelTypeID", inplace=True)
    
    # Get energy consumption values
    energy_sum_dict, fuel_type_dict, energy_consumption_dfs_dict = \
        energy_consumption.get_energy_consumption_values(speeds, number_of_passengers, cycle_location,
                                              year, road_type_id, source_type_id, hours_in_operation,
                                              ambient_temperature_degree_f, relative_humidity, charging_requirement,
                                              all_electric_range_miles, route_length, fuel_type_id_ice,
                                              fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series, no_of_runs_per_day,
                                              power_train_architecture, fuel_type_id_be, fuel_type_id_fce, 
                                              fuel_type_id_pfce, fuel_type_id_phe, city_name, idle_speed_range,fuel_type_id_ice_2,
                                              FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR)
    #
    # We shall represent the emissions output with a dataframe table. The index of the table shall be kind of emission
    # Create the index and columns of the output table
    tech_dictionary={1:1,2:1,3:2,4:9,5:3,6:6,7:7,8:5}  ##[Xiaodan 100115: Warning:!!This is the table need to be updated if the correspondence between vehicle option and fuel technology changes!!]
#    energy_sum_dict=[1,2,3,4,5,6,7,8]
    tech_ids=[]
    for key in energy_sum_dict.keys():
        tech_ids.append(tech_dictionary[key])

  #  print tech_ids
    fuel_upstream_df = pd.DataFrame(columns=energy_sum_dict.keys(), index=c.GHG_EMISSIONS)
 #   print fuel_type_dict
    #fuel_upstream_df["Units"] = c.GHG_EMISSIONS_UNITS
    for emission in c.GHG_EMISSIONS:
        for index, tech_id in enumerate(tech_ids):
            if tech_id not in (7, 5, 3):
#                print tech_id
                fuel_name = fuel_id_name_map_df.loc[fuel_type_dict[index+1]]["FuelTypeGreet"]
                lookup_id = str(fuel_name) + str(year)

                try:
                    fuel_upstream_df[index+1][emission] = float(greet_df.loc[lookup_id][c.GHG_EMISSIONS_SHORTNAMES[emission]]) * energy_sum_dict[index+1] * c.FUEL_UPSTREAM_CALCULATION_CONSTANT
                    
                except Exception as excep:
#                    print e
                    fuel_upstream_df[index+1][emission] = 0.0

    for emission in c.GHG_EMISSIONS: ## EV MODULE
        if emission == c.ATMOSPHERIC_CO2:
            fuel_upstream_df[5][emission]=energy_sum_dict[5] * float(egrid_df.loc[state][c.GHG_EMISSIONS_SHORTNAMES[emission]]) * c.LBS_TO_G /1000
        elif emission in (c.METHANE_CH4, c.NITROUS_OXIDE_N2O):
            fuel_upstream_df[5][emission]=energy_sum_dict[5] * float(egrid_df.loc[state][c.GHG_EMISSIONS_SHORTNAMES[emission]]) * c.LBS_TO_G /1000000
        elif emission in (c.CARBON_MONOXIDE,c.VOLATILE_ORGANIC_COMPOUNDS,c.OXIDES_OF_NITROGEN,c.PRIMARY_EXHAUST_25,c.PRIMARY_EXHAUST_10):
            fuel_upstream_df[5][emission]=energy_sum_dict[5] * float(egrid_df.loc[state][c.GHG_EMISSIONS_SHORTNAMES[emission]]) * c.LBS_TO_G /1000
        elif emission == c.SULPHUR_DIOXIDE_SO2:
            fuel_upstream_df[5][emission]=energy_sum_dict[5] * float(egrid_df.loc[state]["SO2"]) * c.LBS_TO_G /1000
        else:
            fuel_upstream_df[5][emission]=0.0

    for emission in c.GHG_EMISSIONS:
        # Fuel Upstream Plug in Fuel Cell Electric calculation
        if charging_requirement == c.END_OF_RUN:
            if all_electric_range_miles >= route_length:
                fuel_upstream_df[7][emission] = fuel_upstream_df[5][emission]
            else:
                fuel_upstream_df[7][emission] = all_electric_range_miles/route_length*fuel_upstream_df[5][emission] + \
                                              (1-all_electric_range_miles/route_length)*fuel_upstream_df[6][emission]
        else:
            if all_electric_range_miles >= no_of_runs_per_day * route_length:
                fuel_upstream_df[7][emission] = fuel_upstream_df[5][emission]
            else:
                fuel_upstream_df[7][emission] = all_electric_range_miles/(number_of_passengers*route_length)*fuel_upstream_df[5][emission] + \
                                              (1-all_electric_range_miles/route_length)*fuel_upstream_df[6][emission]

        # Fuel Upstream Plug in Hybrid Electric calculation
        if charging_requirement == c.END_OF_RUN:
            if all_electric_range_miles >= route_length:
                fuel_upstream_df[8][emission] = fuel_upstream_df[5][emission]
            else:
                if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                    fuel_upstream_df[8][emission] = all_electric_range_miles/route_length*fuel_upstream_df[5][emission] + \
                    (1-all_electric_range_miles/route_length)*fuel_upstream_df[3][emission]
                else:
                    fuel_upstream_df[8][emission] = all_electric_range_miles/route_length*fuel_upstream_df[5][emission] + \
                    (1-all_electric_range_miles/route_length)*fuel_upstream_df[4][emission]
        else:
            if all_electric_range_miles >= no_of_runs_per_day*route_length:
                fuel_upstream_df[8][emission] = fuel_upstream_df[5][emission]
            else:
                if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                    fuel_upstream_df[8][emission] = all_electric_range_miles/(no_of_runs_per_day * route_length)*fuel_upstream_df[5][emission] + \
                                                (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*fuel_upstream_df[3][emission]
                else:
                    fuel_upstream_df[8][emission] = all_electric_range_miles/(no_of_runs_per_day * route_length)*fuel_upstream_df[5][emission] + \
                    (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*fuel_upstream_df[4][emission]

    fuel_upstream_df.loc[c.ATMOSPHERIC_CO2] = fuel_upstream_df.loc[c.ATMOSPHERIC_CO2]/1000.0
    fuel_upstream_df.loc[c.CO2_EQUIVALENT] = (fuel_upstream_df.loc[c.ATMOSPHERIC_CO2] + fuel_upstream_df.loc[c.METHANE_CH4] * 21.0/1000.0 + \
                                              fuel_upstream_df.loc[c.NITROUS_OXIDE_N2O] * 320.0/1000.0)/1000.0
    #print "hello there"
    # Calculate the emissions output
    # We shall represent the tail pipe emissions output with a dataframe table. The index of the table shall be kind of emission
    # Create the index and columns of the output table
    fuel_tailpipe_df = pd.DataFrame(columns=energy_sum_dict.keys(), index=c.GHG_EMISSIONS)
    #fuel_upstream_df["Units"] = c.GHG_EMISSIONS_UNITS
    emissions = scprec.get_pollutant_emissions(year, road_type_id, source_type_id, fuel_type_dict,
                                               cycle_location, tech_ids, hours_in_operation, energy_consumption_dfs_dict)
    for emission in c.GHG_EMISSIONS:
        for key in energy_sum_dict.keys():
            fuel_name = fuel_id_name_map_df.loc[fuel_type_dict[key]]["FuelTypeGreet"]
            try:
                fuel_tailpipe_df[key][emission] = emissions[key][c.GHG_EMISSIONS_TO_ID_MAP[emission]].sum()
            except Exception as excep:
                fuel_tailpipe_df[key][emission] = 0.0

    for emission in c.GHG_EMISSIONS:
        # Separately calculate for plugin hybrid electric 
        # Fuel Upstream Plug in Hybrid Electric calculation
        if charging_requirement == c.END_OF_RUN:
            if all_electric_range_miles >= route_length:
                fuel_tailpipe_df[8][emission] = fuel_tailpipe_df[5][emission]
            else:
                if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                    fuel_tailpipe_df[8][emission] = all_electric_range_miles/route_length*fuel_tailpipe_df[5][emission] + \
                    (1-all_electric_range_miles/route_length)*fuel_tailpipe_df[3][emission]
                else:
                    fuel_tailpipe_df[8][emission] = all_electric_range_miles/route_length*fuel_tailpipe_df[5][emission] + \
                    (1-all_electric_range_miles/route_length)*fuel_tailpipe_df[4][emission]
        else:
            if all_electric_range_miles >= no_of_runs_per_day*route_length:
                fuel_tailpipe_df[8][emission] = fuel_tailpipe_df[5][emission]
            else:
                if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                    fuel_tailpipe_df[8][emission] = all_electric_range_miles/(no_of_runs_per_day * route_length)*fuel_tailpipe_df[5][emission] + \
                                                (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*fuel_tailpipe_df[3][emission]
                else:
                    fuel_tailpipe_df[8][emission] = all_electric_range_miles/(no_of_runs_per_day * route_length)*fuel_tailpipe_df[5][emission] + \
                    (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*fuel_tailpipe_df[4][emission]


    fuel_tailpipe_df.loc[c.ATMOSPHERIC_CO2] = fuel_tailpipe_df.loc[c.ATMOSPHERIC_CO2]/1000.0
    fuel_tailpipe_df.loc[c.CO2_EQUIVALENT]  = (fuel_tailpipe_df.loc[c.ATMOSPHERIC_CO2] + fuel_tailpipe_df.loc[c.METHANE_CH4] * 21.0/1000.0 + \
                                               fuel_tailpipe_df.loc[c.NITROUS_OXIDE_N2O] * 320.0/1000.0)/1000.0 
    emissions_output_total = fuel_upstream_df + fuel_tailpipe_df
    
    
    # Since for EV the calculation is independent separately put the numbers using the constants in EV sheet
#    for emission_name in emissions_output_total.index:
#        emissions_output_total.ix[emission_name][5] = c.EV_EMISSIONS_MAP[emission_name]
    
    
    loop_df = emissions_output_total
    for emission in c.GHG_EMISSIONS:
        # Fuel Upstream Plug in Fuel Cell Electric calculation
        if charging_requirement == c.END_OF_RUN:
            if all_electric_range_miles >= route_length:
                loop_df[7][emission] = loop_df[5][emission]
            else:
                loop_df[7][emission] = all_electric_range_miles/route_length*loop_df[5][emission] + \
                                              (1-all_electric_range_miles/route_length)*loop_df[6][emission]
        else:
            if all_electric_range_miles >= no_of_runs_per_day * route_length:
                loop_df[7][emission] = loop_df[5][emission]
            else:
                loop_df[7][emission] = all_electric_range_miles/(number_of_passengers*route_length)*loop_df[5][emission] + \
                                              (1-all_electric_range_miles/route_length)*loop_df[6][emission]
    
    
    for emission in c.GHG_EMISSIONS:
        # Separately calculate for plugin hybrid electric 
        # Fuel Upstream Plug in Hybrid Electric calculation
        if charging_requirement == c.END_OF_RUN:
            if all_electric_range_miles >= route_length:
                loop_df[8][emission] = loop_df[5][emission]
            else:
                if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                    loop_df[8][emission] = all_electric_range_miles/route_length*loop_df[5][emission] + \
                    (1-all_electric_range_miles/route_length)*loop_df[3][emission]
                else:
                    loop_df[8][emission] = all_electric_range_miles/route_length*loop_df[5][emission] + \
                    (1-all_electric_range_miles/route_length)*loop_df[4][emission]
        else:
            if all_electric_range_miles >= no_of_runs_per_day*route_length:
                loop_df[8][emission] = loop_df[5][emission]
            else:
                if power_train_architecture == c.TRAIN_ARCHITECTURE_PARALLEL:
                    loop_df[8][emission] = all_electric_range_miles/(no_of_runs_per_day * route_length)*loop_df[5][emission] + \
                                                (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*loop_df[3][emission]
                else:
                    loop_df[8][emission] = all_electric_range_miles/(no_of_runs_per_day * route_length)*loop_df[5][emission] + \
                    (1-all_electric_range_miles/(no_of_runs_per_day * route_length))*loop_df[4][emission]

###Edit the unit##        
    annual_total_emissions = emissions_output_total * number_of_runs_per_bus_per_year * number_of_buses
    for emission in c.GHG_EMISSIONS:
        if emission in (c.CARBON_MONOXIDE,c.VOLATILE_ORGANIC_COMPOUNDS,c.OXIDES_OF_NITROGEN,c.PRIMARY_EXHAUST_25,c.PRIMARY_EXHAUST_10, c.SULPHUR_DIOXIDE_SO2):
            for i in range(8):
                annual_total_emissions[i+1][emission] = annual_total_emissions[i+1][emission]/1000
    
    unit_total=pd.Series(c.GHG_EMISSIONS_UNITS,index=c.GHG_EMISSIONS)
    unit_annual=pd.Series(c.ANNUAL_GHG_EMISSIONS_UNITS,index=c.GHG_EMISSIONS)
    fuel_upstream_df.insert(0,'unit',unit_total)
    fuel_tailpipe_df.insert(0,'unit',unit_total)
    emissions_output_total.insert(0,'unit',unit_total)
    annual_total_emissions.insert(0,'unit',unit_annual)
 #   print annual_total_emissions
#    util.df_to_csv_debug(annual_total_emissions,"annual_total_emission.csv")
#    util.df_to_csv_debug(emissions_output_total,"emissions_output_total.csv")
#    util.df_to_csv_debug(fuel_tailpipe_df,"fuel_tailpipe.csv")
#    util.df_to_csv_debug(fuel_upstream_df,"fuel_upstream.csv")
    return fuel_upstream_df, fuel_tailpipe_df, emissions_output_total, annual_total_emissions, energy_sum_dict
    

# <codecell>

# emissions_output_total, annual_total_emissions, energy_sum_dict = get_emissions(cycle_name, number_of_passengers, cycle_location, year, road_type_id, source_type_id, hours_in_operation,
#                   ambient_temperature_degree_f, relative_humidity, charging_requirement, all_electric_range_miles,
#                   route_length, fuel_type_id_ice, fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series,
#                   no_of_runs_per_day, power_train_architecture, fuel_type_id_be, fuel_type_id_fce, 
#                   fuel_type_id_pfce, fuel_type_id_phe, number_of_runs_per_bus_per_year, number_of_buses, city_name)

# <codecell>

# emissions_output_total

# <codecell>


