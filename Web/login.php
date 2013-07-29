<?php
/**
 * Created by JetBrains PhpStorm.
 * User: Joey
 * Date: 6/24/13
 * Time: 9:56 AM
 * To change this template use File | Settings | File Templates.
 */
require_once 'data/settings.php';

$username = mysql_real_escape_string($_GET['username']);
$password = mysql_real_escape_string($_GET['password']);

@$row = sqlite_fetch_array(sqlite_query("SELECT id, password FROM accounts WHERE username = '".$username."'"));
if($row['password'] == md5($password)) {
    $sid = md5($password).sha1($row['id']);
    sqlite_query("UPDATE accounts SET sid='".$sid."' WHERE username = '".$username."'");
    setcookie("sid", $sid);
    setcookie("uid", $row['id']);
    header("Location: dashboard.html");
} else {
    header("Location: index.php?badlogin=true");
}