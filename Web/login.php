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

$row = mysql_fetch_assoc(mysql_query("SELECT id, password FROM users WHERE username = '".$username."'"));
if($row = md5($password)) {
    header("Location: dashboard.html");
} else {
    echo "Incorrect username/password combination";
}