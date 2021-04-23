<?php


$url = 'http://rg49-web3.ce.gatech.edu/bus/python_code/call_python.php';

// use key 'http' even if you send the request to https://...
$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($_POST),
    ),
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);

echo($result);



//~ print ' python ./python_gateway.py ' . $arg_str
?>