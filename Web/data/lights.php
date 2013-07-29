<?php
require_once 'settings.php';

function getLights() {
    $lightquery = sqlite_query("SELECT pin,name FROM outputs");
    $data = array();
    while($row = sqlite_fetch_array($lightquery)) {
        $data[] = $row;
    }
    if($data == []) {
        $data[] = array("name"=> "No Lights",
                        "pin" => "-");
    }
    return json_encode($data);
}

if(isset($_GET['action']) && $_GET['action'] == "getlights") {
    echo getLights();
}