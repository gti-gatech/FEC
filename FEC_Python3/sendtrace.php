<?php
//$fileName = $_FILES['traces']['name'];
//$fileType = $_FILES['traces']['type'];
//$fileContent = file_get_contents($_FILES['traces']['tmp_name'])
$target_dir = "tmp/";
$target_file = $target_dir . basename($_FILES['traces']['name']);
//$uploadOk = 1;
if (move_uploaded_file($_FILES['traces']["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES['traces']["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
//$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is a actual image or fake image
/*
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}
$fp = fopen($_FILES['traces']['tmp_name'], 'r') or die("Unable to open file!");
*/
//$command = escapeshellcmd(' http://rg49-web3.ce.gatech.edu/bus/python_code/python ./trace_process.py ' . $fp);
//echo <p> fread($fp,filesize($_FILES['traces']['tmp_name'])) </p>;	

?>
