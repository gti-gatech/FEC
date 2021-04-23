<?php
$csv = array_map('str_getcsv', file("CityLookup.csv"));
//var_dump($csv);
echo json_encode(array_slice($csv, 1));


?>
