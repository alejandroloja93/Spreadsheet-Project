<html>
<body>
  <button type="button" id="submit1" onclick="submit();">Submit</button>
  /**
  *
  *Displays different values based on the floor function on the local server
  */
	<?php
	$array = Array(
		Array('Data','','max ='),
		Array('=FLOOR(10*SIN(RAND()*PI()/2);1)','','min ='),
		Array('=FLOOR(10*SIN(RAND()*PI()/2);1)','','total ='),
		Array('=FLOOR(10*SIN(RAND()*PI()/2);1)','','number of data ='),
		Array('=FLOOR(10*SIN(RAND()*PI()/2);1)','','mean ='),
		Array('=FLOOR(10*SIN(RAND()*PI()/2);1)','','median ='),
		Array('=FLOOR(10*SIN(RAND()*PI()/2);1)','','mode ='),
	);
	for( $i=7;$i<51;$i++){
		$array[] = Array('=FLOOR(10*SIN(RAND()*PI()/2);1)');
		}

	$data_encoded = base64_encode(json_encode($array));
	$data_encoded = escapeshellcmd($data_encoded);
	#Requires appropriate path
	$pyscript = 'python where_are_data.py';
	$command = escapeshellcmd("$pyscript");
	$output = (array)json_decode(shell_exec("$command  '{$data_encoded}'"));
	echo "<iframe src='{$output['full_url']}' height='100%' width='100%'></iframe>";

	?>
<!--SUBMIT FUNCTION-->
<!-- Includes jQUERY LIBRARY -->
<script src="http://code.jquery.com/jquery-latest.min.js"
      type="text/javascript"></script>
<!-- Call jQuery server via AJAX-->
  <script type="text/javascript">   //ß
    function submit(){
		$.ajax({
			type: "POST",
			<!--Requires appropriate path-->
			url: 'ConnectDB.php',
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
