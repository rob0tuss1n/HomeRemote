<?php
/**
 * Created by JetBrains PhpStorm.
 * User: Joey
 * Date: 6/25/13
 * Time: 2:09 PM
 * To change this template use File | Settings | File Templates.
 */
require_once 'settings.php';

function checkAuth() {
    if(!isset($_COOKIE['sid']) || !isset($_COOKIE['uid'])) {
        return "false";
    }
    $sid = $_COOKIE['sid'];
    $realsid = mysql_fetch_assoc(mysql_query("SELECT sid, name FROM accounts WHERE id='".$_COOKIE['uid']."'"));
    if($realsid['sid'] == $sid) {
        return $realsid['name'];
    } else {
        return "false";
    }
}
if($_GET['action']=="checkauth") {
    echo checkAuth();
} elseif($_GET['action'] == "logout") {
    setcookie ("sid", "", time() - 3600);
    setcookie ("uid", "", time() - 3600);
    header("Location: index.php");
}