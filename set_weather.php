<?php

	echo "START OF SCRIPT - ".date('r')."\n";
	echo "-----------------------------------------------------------------------------------------------------\n\n";

	require("/root/.mc_server.php");
	if(file_exists("/usr/local/bin/mcrcon")) {
		$mcrconLocation = "/usr/local/bin/mcrcon";
	} else {
		echo "Could not find mcrcon file!\n";exit;
	}

	$previousWeather = "/root/.mc_weather";

	$apiKey = "220ede2aed4da7138aa64f545f8316bd";
	$exclusions = "hourly,minutely,daily";
	$lat = "36.0178911";
	$long = "-78.8083965";
	$url = "https://api.openweathermap.org/data/2.5/onecall?lat=$lat&lon=$long&exclude=$exclusions&appid=$apiKey";

	$jsonData = file_get_contents($url);
	$data = json_decode($jsonData, true);

	foreach($data as $key=>$value) {
		if($key == "current") {
			foreach($value as $k=>$v) {
				if($k == "weather") {
					foreach($v[0] as $item=>$element) {
						if($item == "main") {
							$weather = $element;
							if($weather == "Clear" || $weather == "Clouds") {
								echo "Setting Owencraft to clear for the next hour\n";
								$currentWeather = file_get_contents($previousWeather);
								if($currentWeather == $weather) {
									$setWeather = file_put_contents("$previousWeather", $weather);
								} else {
									$cmd = "$mcrconLocation -H $mc_server -p $mc_password \"weather clear 3600\"";
									$exec = exec($cmd,$output,$return);
									$setWeather = file_put_contents("$previousWeather", $weather);
								}
							} elseif($weather == "Rain" || $weather == "Drizzle" || $weather == "Snow") {
								echo "Setting Owencraft to rain for the next hour\n";
								$currentWeather = file_get_contents($previousWeather);
								if($currentWeather == $weather) {
									$setWeather = file_put_contents("$previousWeather", $weather);
								} else {
									$cmd = "$mcrconLocation -H $mc_server -p $mc_password \"weather rain 3600\"";
									$exec = exec($cmd,$output,$return);
									$setWeather = file_put_contents("$previousWeather", $weather);
								}
							} elseif($weather == "Thunderstorm") {
								echo "Setting Owencraft to rain for the next hour\n";
								$currentWeather = file_get_contents($previousWeather);
								if($currentWeather == $weather) {
									$setWeather = file_put_contents("$previousWeather", $weather);
								} else {
									$cmd = "$mcrconLocation -H $mc_server -p $mc_password \"weather rain 3600\"";
									$exec = exec($cmd,$output,$return);
									$setWeather = file_put_contents("$previousWeather", $weather);
								}
							} else {
								echo "Unable to determine weather, setting to clear for the next hour\n";
								$cmd = "$mcrconLocation -H $mc_server -p $mc_password \"weather clear 3600\"";
								$exec = exec($cmd,$output,$return);
								$setWeather = file_put_contents("$previousWeather", "Clear");
							}
						}
					}
				}
			}
		}
	}

	echo "\n-----------------------------------------------------------------------------------------------------\n";
	echo "END OF SCRIPT - ".date('r')."\n";

?>
