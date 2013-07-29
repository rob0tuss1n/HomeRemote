<?php
require_once 'settings.php';

function getInputs() {
    $eventquery = sqlite_query("SELECT * FROM inputs");
    while($row = sqlite_fetch_array($eventquery)) {
        $data[] = $row;
    }
    return json_encode($data);
}

if(isset($_GET['action']) && $_GET['action'] == "getinputs") {
    echo getInputs();
}