<?php
require_once 'settings.php';
function getSysTime() {
    return date("g:i A, M d Y");
}
function getUnusedInputs() {
    $query =mysql_query("SELECT * FROM pins WHERE used = '0'");
    while($row = mysql_fetch_assoc($query)) {
        $data[] = $row;
    }
    return json_encode($data);
}
if($_GET['action'] == "gettime") {
    echo getSysTime();
}
elseif($_GET['action'] == "getunusedinputs") {
    echo getUnusedInputs();
}