<html>
<body>
  //This submit function produces a submit button the local server.
  <button type="button" id="submit1" onclick="submit();">Submit</button>
  /**
  *
  * Displays random valuyes from 1 to 10 on
  * different cells on the local server
  */
<?php
$array = Array(
	Array("A","B","C","Totals"),
	Array(rand(1,10), rand(1,10), rand(1,10), '=SUM(A2:C2)'),
	Array(rand(1,10), rand(-10,10), rand(1,10), "=SUM(A3:C3)"),
	Array(rand(1,10), rand(1,10), rand(1,10), "=SUM(A4:C4)")
);


$data_encoded = base64_encode(json_encode($array));
$data_encoded = escapeshellcmd($data_encoded);
$pyscript = 'python /Applications/MAMP/htdocs/where_are_data.py';
$command = escapeshellcmd("$pyscript");
$output = (array)json_decode(shell_exec("$command  '{$data_encoded}'"));
echo "<iframe src='{$output['full_url']}' height='100%' width='100%'></iframe>";

?>

<!-- Includes jQUERY LIBRARY -->
<script src="http://code.jquery.com/jquery-latest.min.js"
      type="text/javascript"></script>
<!-- Call jQuery server via AJAX-->
  <script type="text/javascript">   //ß
    function submit(){
      $.ajax({
          type: "POST",
          url: 'Database.php',
          async: false,
          cache: false,
          data: ({
            'id' : '<?php print $output['id'] ?>'
          }),
          success: function(data){
            alert(data);
          }

        });
      }
</script>

</body>
</html>
