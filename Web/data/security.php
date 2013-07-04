<?php
/**
 * Created by JetBrains PhpStorm.
 * User: Joey
 * Date: 6/25/13
 * Time: 1:12 PM
 * To change this template use File | Settings | File Templates.
 */
require_once 'settings.php';
if(!isset($_GET['action'])) {
    $_GET['action'] = "none";
}
function getCameraFeeds() {
    $sql = mysql_query("SELECT * FROM security_cameras");
    while($row = mysql_fetch_assoc($sql)) {
        $feeds[] = $row;
    }
    return json_encode($feeds);
}
function getSnapNames($folder) {
    return json_encode(scandir("/usr/share/nginx/www/cams/".$folder));
}
function getUnusedCams() {
    $sql = mysql_query("SELECT video_device FROM security_cameras");
    while($row = mysql_fetch_assoc($sql)) {
        $data[] = $row;
    }
    return json_encode($data);
}
if($_GET['action'] == "getcamerafeeds") {
    echo getCameraFeeds();
} elseif($_GET['action'] == "getsnapnames") {
    echo getSnapNames($_GET['folder']);
}