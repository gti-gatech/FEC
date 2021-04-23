<?php 
//cycle_name, number_of_passengers, cycle_location,\
//year, road_type_id, source_type_id, hours_in_operation,\
//ambient_temperature_degree_f, relative_humidity, charging_requirement,\
//all_electric_range_miles, route_length, fuel_type_id_ice,\
//fuel_type_id_hybrid_parallel, fuel_type_id_hybrid_series, no_of_runs_per_day,\
//power_train_architecture, fuel_type_id_be, fuel_type_id_fce, fuel_type_id_pfce,\
//fuel_type_id_phe


//~ var_dump($_POST);
$cycle_name = $_POST["cycle_name"];
$number_of_passengers = $_POST["number_of_passengers"];
$year = $_POST["year"];
$road_type_id = $_POST["road_type_id"];
$source_type_id = $_POST["source_type_id"];
$season = $_POST["season"];
$severity = $_POST["severity"];
$charging_requirement = $_POST["charging_requirement"];
$all_electric_range_miles = $_POST["all_electric_range_miles"];
$route_length = $_POST["route_length"];
$idle_speed_range =$_POST["idle_speed_range"];
$fuel_type_id_ice = $_POST["fuel_type_id_ice"];
$fuel_type_id_ice_2 = $_POST["fuel_type_id_ice_2"];
$fuel_type_id_hybrid_parallel = $_POST["fuel_type_id_hybrid_parallel"];
$fuel_type_id_hybrid_series = $_POST["fuel_type_id_hybrid_series"];
$no_of_runs_per_day = $_POST["no_of_runs_per_day"];
$power_train_architecture = $_POST["power_train_architecture"];
$fuel_type_id_be = $_POST["fuel_type_id_be"];
$fuel_type_id_fce = $_POST["fuel_type_id_fce"];
$fuel_type_id_pfce = $_POST["fuel_type_id_pfce"];
$fuel_type_id_phe = $_POST["fuel_type_id_phe"];
$number_of_runs_per_bus_per_year =  $_POST["number_of_runs_per_bus_per_year"];
$number_of_buses = $_POST["number_of_buses"];
$city = $_POST["city"];
//~ $args = array("HD-UDDS",
         //~ "0",
         //~ "1", 
         //~ "2011",
         //~ "5",
         //~ "42",
         //~ "0.530337825194649", "87.3", "53.8", "End_of_Run",
         //~ "5.0", "10.0", "2", "2", "2", 
         //~ "10", "Series", "2", "0", "0", "2");

$arg_str = join("    ", array($cycle_name,
                      $number_of_passengers,
                      $year,
                      $road_type_id,
                      $source_type_id,
					  $season,
					  $severity,
                      $charging_requirement,
                      $all_electric_range_miles,
                      $route_length,
					  $idle_speed_range,
                      $fuel_type_id_ice,
					  $fuel_type_id_ice_2,
                      $fuel_type_id_hybrid_parallel,
                      $fuel_type_id_hybrid_series,
                      $no_of_runs_per_day,
                      $power_train_architecture,
                      $fuel_type_id_be,
                      $fuel_type_id_fce,
                      $fuel_type_id_pfce,
                      $fuel_type_id_phe,
                      $number_of_runs_per_bus_per_year,
                      $number_of_buses,
                      $city));

//~ var_dump($arg_str);
$command = escapeshellcmd(' python ./fec_gateway.py ' . $arg_str);
//$myfile = fopen("python_command_executed.txt", "w") or die("Unable to open file!");
//fwrite($myfile, $command);
//fclose($myfile);
$output = shell_exec($command);
print($output);
//~ print ' python ./python_gateway.py ' . $arg_str
?>
