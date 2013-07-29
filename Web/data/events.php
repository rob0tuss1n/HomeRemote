<?php
require_once 'settings.php';

function getEvents() {
    $eventquery = sqlite_query("SELECT * FROM events");
    $data = array();
    while($row = sqlite_fetch_array($eventquery)) {
        $data[] = $row;
    }
    return json_encode($data);
}

if($_GET['action'] == "getevents") {
    echo getEvents();
}