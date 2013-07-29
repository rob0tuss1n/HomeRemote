<?php
require_once 'settings.php';
function getWeather() {
    $id = sqlite_fetch_assoc(sqlite_query("SELECT value FROM settings WHERE field = 'city_id'"));
    $data = (array) json_decode(file_get_contents("http://api.openweathermap.org/data/2.5/weather?id=".$id['value']));
    foreach($data as $key => $sub) {
        if(is_object($sub)) {
            $data[$key] = (array) $sub;
        }
    }
    $data['weather']['0'] = (array) $data['weather']['0'];
    $data['sys']['sunrise'] = date('g:i A', $data['sys']['sunrise']);
    $data['sys']['sunset'] = date('g:i A', $data['sys']['sunset']);
    $data['dt'] = date('g:i A M d Y', $data['dt']);
    $data['main']['temp'] = number_format(($data['main']['temp'] - 273.15) * 9 / 5 + 32, 0, '.', '');
    $data['main']['temp_min'] = number_format(($data['main']['temp_min'] - 273.15) * 9 / 5 + 32, 0, '.', '');
    $data['main']['temp_max'] = number_format(($data['main']['temp_max'] - 273.15) * 9 / 5 + 32, 0, '.', '');
    return $data;
}

function searchCity($string) {
    $string = str_replace(" ", "%20", $string);
    $data = (array) json_decode(file_get_contents("http://api.openweathermap.org/data/2.5/find?q=".$string."&type=like"));
    foreach($data['list'] as $key => $sub) {
        if(is_object($sub)) {
            $data['list'][$key] = (array) $sub;
        }
        unset($data['list'][$key]['weather']);
        unset($data['list'][$key]['clouds']);
        unset($data['list'][$key]['sys']);
        unset($data['list'][$key]['dt']);
        unset($data['list'][$key]['wind']);
        unset($data['list'][$key]['main']);
        unset($data['list'][$key]['coord']);
        unset($data['list'][$key]['rain']);
    }
    return $data['list'];
}

if($_GET['action'] == 'search' && isset($_GET['str'])) {
    echo json_encode(searchCity($_GET['str']));
} elseif($_GET['action'] == 'getweather') {
    echo json_encode(getWeather());
}

?>