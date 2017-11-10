<?php
	
	// look through logs to find an incremental number to mark this log
	$k = 0;

	while (file_exists('logs/'.$k)) {
	    $k++;
	}

	// write contents of post request to file
	file_put_contents('logs/'.$k, file_get_contents("php://input"));
?>