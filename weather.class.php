<?php

    require_once __DIR__ . "/logging.class.php";
    require_once __DIR__ . "/mcron.class.php";

    class owencraft_weather {

        public $SCHEMA = "https://";
        public $DOMAIN = "api.openweathermap.org";
        public $VERSION = "2.5";
        private $apikey;
        public $latitude;
        public $longitude;
        public $exclusions;

        public $log_path = __DIR__;
        public $log_file = "/weather.log";
        public $logger;

        private $mcrcon;

        function __construct($file) {
            $this->logger = new oclogger($this->log_path, $this->log_file);
            $this->mcrcon = new mcrcon();
            if(file_exists($file)) {
                $this->apikey = rtrim(file_get_contents($file));
            } else {
                $this->logger->logMsg("Unable to locate API Key!", 2);
                exit;
            }
        }

        public function setLocation(string $lat, string $long) {
            /*
                Use this method to set the location for where you want to get the weather from
            */
            $this->latitude = $lat;
            $this->longitude = $long;
        }

        public function setExclusions(array $exc) {
            /*
                Use this method to set the exclusions on what data you want returned from the API call
            */
            $len = count($exc);
            if($len === 0) {
                $this->exclusions = FALSE;
            } else {
                $exclusion_list = "";
                $i = 0;
                while($i < $len) {
                    if($len === 1) {
                        $exclusion_list = $exc[$i];
                    } elseif($i === ($len - 1)) {
                        $exclusion_list = $exclusion_list . $exc[$i];
                    } else {
                        $exclusion_list = $exclusion_list . $exc[$i] . ",";
                    }
                    $i++;
                }
                $this->exclusions = $exclusion_list;
            }
        }

        public function callApi() {
            /*
                Use this method to call the OpenWeatherMap API using the class objects as variables
            */
            $url = "{$this->SCHEMA}{$this->DOMAIN}/data/{$this->VERSION}/onecall?lat={$this->latitude}&lon={$this->longitude}&exclude={$this->exclusions}&appid={$this->apikey}";
            $ch = curl_init();
            if(!$ch) {
                $this->logger->logMsg("Unable to initialize CURL!", 2);
                return FALSE;
            }
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            $response = curl_exec($ch);
            if(!curl_errno($ch)) {
                switch($status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE)) {
                    case 200:
                        return $response;
                    default:
                        $this->logger->logMsg("API Call failed! URL: {$url} :: Status: {$status_code} :: Extra Data: {$response}", 2);
                        return FALSE;
                }
            }
            curl_close($ch);
        }

        public function getWeather(string $data) {
            /*
                Use this method to parse the JSON results from the callApi() method and return the weather
            */
            // https://openweathermap.org/api/one-call-3#example
            $json_data = json_decode($data, TRUE); // get a multi-dimensional array of the data we need
            if($json_data["current"]["weather"][0]["main"]) {
                return $json_data["current"]["weather"][0]["main"];
            } else {
                $this->logger->logMsg("Unable to parse JSON Response Data! Data: {$data}", 2);
                return FALSE;
            }
        }

        public function setWeather(string $current_weather) {
            /*
                Use this method as a wrapper to mcrcon class from owencraft-stats repo
                You could write your own mcrcon wrapper here instead
            */
            if($current_weather === "Clear" || $current_weather === "Clouds") {
                $msg = "Setting weather to Clear!";
                $this->logger->logMsg($msg, 0);
                $this->mcrcon->setWeather("clear");
            } elseif($current_weather === "Rain" || $current_weather === "Drizzle" || $current_weather === "Snow" || $current_weather === "Thunderstorm") {
                $msg = "Setting weather to Rain!";
                $this->logger->logMsg($msg, 0);
                $this->mcrcon->setWeather("rain");
            } else {
                $msg = "Unable to determine weather conditions! Clearing weather for now...";
                $this->logger->logMsg($msg, 0);
                $this->mcrcon->setWeather("clear");
            }
        }

    }

?>