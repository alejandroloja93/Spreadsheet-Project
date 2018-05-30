<html>
<body>


<?php
/**
*
*
*Identifies which ID to use from the database
*Gets the results from the database
*/
$id = 28;
$con = mysqli_connect('localhost', 'root', 'root');
  if(!$con){
    die('Could not connect to DB: ' .mysqli_error());
  }

  mysqli_select_db($con,'SpreadSheetDB');
  $query = "SELECT Value FROM SSData WHERE id=$id";
  $result = mysqli_query($con, $query) or die("Failed");
  $row = mysqli_fetch_assoc($result);
  //echo "Success".json_encode($row);
  $array = json_decode($row['Value']);
  var_dump($array);

//$out = array_values($array);
//$result = cmd_exec("Python where_are_data.py ". escapeshellcmd(json_encode($out)) . "'");
//$resultData = json_decode($result, true);
//var_dump($resultData);

/**
*
* Displays the results on the local server 
*/

$data_encoded = base64_encode(json_encode($array));
$data_encoded = escapeshellcmd($data_encoded);
$pyscript = 'python /Applications/MAMP/htdocs/where_are_data.py';
$command = escapeshellcmd("$pyscript");
$output = (array)json_decode(shell_exec("$command  '{$data_encoded}'"));
echo "<iframe src='{$output['full_url']}' height='100%' width='100%'></iframe>";

?>



</body>
</html>
