<?php
require_once 'data/settings.php';

$username = $_GET['username'];
$password = $_GET['password'];

@$row = $GLOBALS['db']->custom_query("SELECT id, password FROM accounts WHERE username = '".$username."'");
if($row[0]['password'] == md5($password)) {
    $sid = md5($password).sha1($row[0]['id']);
    $GLOBALS['db']->insert_query("UPDATE accounts SET sid='".$sid."' WHERE username = '".$username."'");
    setcookie("sid", $sid);
    setcookie("uid", $row[0]['id']);
    header("Location: dashboard.html");
} else {
    header("Location: index.php?badlogin=true");
}