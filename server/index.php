<?php

	$stateFile = 'starttime.txt';
	$timeToBrew = 240;

	if (!empty($_GET['state'])) {

		if ($_GET['state'] == 'ON') {

			$f = fopen($stateFile, 'w+');
			fwrite($f, 'ON;'.time());
			fclose($f);

		} else if ($_GET['state'] == 'OFF') {

			$f = fopen($stateFile, 'w+');
			fwrite($f, 'OFF;'.time());
			fclose($f);

		}

	}

	if (file_exists($stateFile)) {

		$f = fopen($stateFile, 'r');
		$state = fread($f, filesize($stateFile));
		fclose($f);
		
		$stateArray = explode(';', $state);

		echo $stateArray[0].';'.(time() - $stateArray[1]);

	}

?>
