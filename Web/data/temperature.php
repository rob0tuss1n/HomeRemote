<?php
require 'settings.php';
function get24hdata() {
    $sql = "SELECT temp, date, pin FROM temperature_records WHERE temperature_records.`date` > DATE_SUB(CURDATE(), INTERVAL 1 DAY)";
    $data = array();
    while($row = $db->select($sql)) {
        $data[] = $row;
    }
    foreach($data as $record) {
        $name = $db->select("SELECT name FROM inputs WHERE pin = '".$record['pin']."'");
        $record['name'] = $name['name'];
    }
    return json_encode($data);
}
if($_GET['action'] == "get24hdata") {
    echo get24hdata();
}