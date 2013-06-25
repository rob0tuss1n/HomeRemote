<?php
require_once 'settings.php';

function getLights() {
    $lightquery = mysql_query("SELECT pin,name FROM lights");
    $data = array();
    while($row = mysql_fetch_assoc($lightquery)) {
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