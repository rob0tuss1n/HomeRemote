<?php
require_once 'settings.php';

function getEvents() {
    $eventquery = mysql_query("SELECT * FROM events1");
    $data = array();
    while($row = mysql_fetch_assoc($eventquery)) {
        $data[] = $row;
    }
    return json_encode($data);
}

if($_GET['action'] == "getevents") {
    echo getEvents();
}