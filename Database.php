<?php
$id = $_REQUEST['id'];
$data_encoded = base64_encode(json_encode($id));
$data_encoded = escapeshellcmd($data_encoded);
$pyscript = 'python /Applications/MAMP/htdocs/data_2.py';
$command = escapeshellcmd("$pyscript");
$output = shell_exec("$command  '{$data_encoded}'");
//Make database here
//write my insert query

/**
*
* Connects to the database
*Requires the local host name, database username and password to connect
*If it connects to the database, it shows the results
*/

echo $output;
$con = mysqli_connect('localhost', 'root', 'root');
  if(!$con){
    die('Could not connect to DB: ' .mysqli_error());
  }

  mysqli_select_db($con,'SpreadSheetDB');
  $query = "INSERT INTO SSData (Value) VALUES ('$output')";
  $result = mysqli_query($con, $query) or die("Failed");
  echo "Success".json_encode($result);

?>
