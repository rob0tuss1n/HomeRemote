<?php
/**
 * Created by JetBrains PhpStorm.
 * User: Joey
 * Date: 6/24/13
 * Time: 9:56 AM
 * To change this template use File | Settings | File Templates.
 */
require_once 'data/settings.php';

$username = $_GET['username'];
$password = $_GET['password'];

@$row = mysql_fetch_assoc(mysql_query("SELECT id, password FROM accounts WHERE username = '".$username."'"));
if($row['password'] == md5($password)) {
    $sid = md5($password).sha1($row['id']);
    mysql_query("UPDATE accounts SET sid='".$sid."' WHERE username = '".$username."'");
    setcookie("sid", $sid);
    setcookie("uid", $row['id']);
    header("Location: dashboard.html");
} else {
    header("Location: index.php?badlogin=true");
}