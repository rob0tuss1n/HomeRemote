<?php
require_once 'settings.php';

function getEvents() {
    $eventquery = "SELECT * FROM events";
    $data = array();
    $data = $GLOBALS['db']->select($eventquery));
    if($data == []) {
        $data[] = array("name"=> "No Events",
                        "id" => "-");
    }
    return json_encode($data);
}

if($_GET['action'] == "getevents") {
    echo getEvents();
}