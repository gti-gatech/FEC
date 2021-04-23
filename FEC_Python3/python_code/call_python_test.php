<?php 
//cycle_name, number_of_passengers, cycle_location,\
//year, road_type_id, source_type_id, hours_in_operation,\
//ambient_temperature_degree_f, relative_humidity, charging_requirement,\
//all_electric_range_miles, route_length, fuel_type_id_ice,\
//fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series, no_of_runs_per_day,\
//power_train_architecture, fuel_type_id_be, fuel_type_id_fce, fuel_type_id_pfce,\
//fuel_type_id_phe
$args = array(" HD-UDDS ",
         " 0 ",
         " 1 ", 
         " 2011 ",
         " 5 ",
         " 42 ",
         " 0.530337825194649 ", " 87.3 ", " 53.8 ", " End_of_Run ",
         " 5.0 ", " 10.0 ", " 2 ", " 2 ", " 2 ", 
         " 10 ", " Series ", " 2 ", " 0 ", " 0 ", " 2 ");
$command = escapeshellcmd(' python ./python_gateway.py HD-UDDS    0    1    2010    5    42    0.530337825194649    87.3    53.8    End_of_Run    5    10    1    1    1    10    Series    1    1    1    1    3650    500');
$output = shell_exec($command);
echo $output;
#echo ' python ./python_code/python_gateway.py ' . "   ".join($args);
?>
