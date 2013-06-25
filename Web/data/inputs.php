<?php
require_once 'settings.php';

function getInputs() {
    $eventquery = mysql_query("SELECT * FROM inputs");
    while($row = mysql_fetch_assoc($eventquery)) {
        $data[] = $row;
    }
    return json_encode($data);
}

if(isset($_GET['action']) && $_GET['action'] == "getinputs") {
    echo getInputs();
}