<?php

	require_once __DIR__ . "/weather.class.php";
	require_once "/home/benjamin/Documents/github/owencraft-stats/logging.class.php";

	$file = __DIR__ . "/.creds";
	$weather = new owencraft_weather($file);

	$weather->logger->startScript();

	$lat = "36.0178911";
	$long = "-78.8083965";
	$msg = "Setting Latitude to {$lat} and setting Longitude to {$long}...";
	$weather->logger->logMsg($msg, 0);
	$weather->setLocation($lat, $long);

	$exclusions = array("hourly", "minutely", "daily");
	foreach ($exclusions as $exclusion) {
		$msg = "Setting exclusion: {$exclusion}...";
		$weather->logger->logMsg($msg, 0);
	}
	$weather->setExclusions($exclusions);

	$msg = "Calling API...";
	$weather->logger->logMsg($msg, 0);
	$raw_data = $weather->callApi();
	if($raw_data) {
		$msg = "Successfully received weather data from API! Parsing results for the current weather...";
		$weather->logger->logMsg($msg, 0);
		$current_weather = $weather->getWeather($raw_data);
	} else {
		$msg = "Unable to get weather data from API! Cannot continue!";
		$weather->logger->logMsg($msg, 2);
		exit(1);
	}

	if($current_weather) {
		$msg = "The current weather is: {$current_weather}!";
		$weather->logger->logMsg($msg, 0);
	} else {
		$msg = "Unable to retrieve the current weather!";
		$weather->logger->logMsg($msg, 2);
	}

	$msg = "Calling mcrcon to set the weather on the server...";
	$weather->logger->logMsg($msg, 0);
	$weather->setWeather($current_weather);

	$weather->logger->stopScript();

?>
