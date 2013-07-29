<?php
require_once 'settings.php';
function getSysTime() {
    return date("g:i A, M d Y");
}
function getUnusedInputs() {
    $query =sqlite_query("SELECT * FROM pins WHERE used = '0'");
    while($row = sqlite_fetch_array($query)) {
        $data[] = $row;
    }
    return json_encode($data);
}
function getMotionStatus() {
    if(file_exists("/var/run/motion/motion.pid")) {
        return "camera server <b>running</b>";
    } else {
        return "camera server <b>not running</b>";
    }
}
if($_GET['action'] == "gettime") {
    echo getSysTime();
}
elseif($_GET['action'] == "getunusedinputs") {
    echo getUnusedInputs();
}
elseif($_GET['action'] == "getmotionstatus") {
    echo getMotionStatus();
}