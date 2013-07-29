<?php
require 'settings.php';
function get24hdata() {
    $sql = sqlite_query("SELECT temp, date, pin FROM temperature_records WHERE temperature_records.`date` > DATE_SUB(CURDATE(), INTERVAL 1 DAY)");
    $data = array();
    while($row = mysql_fetch_assoc($sql)) {
        $data[] = $row;
    }
    foreach($data as $record) {
        $name = sqlite_fetch_array(sqlite_query("SELECT name FROM inputs WHERE pin = '".$record['pin']."'"));
        $record['name'] = $name['name'];
    }
    return json_encode($data);
}
if($_GET['action'] == "get24hdata") {
    echo get24hdata();
}