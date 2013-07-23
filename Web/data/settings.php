<?php
$sqlhost = "localhost";
$sqluser = "root";
$sqlpass = "";
$sqldb = "automation";

$websockserver = "192.168.1.68";
$websockport = "9000";

// Dont edit anything below here unless you know what your doing!

mysql_connect($sqlhost, $sqluser, $sqlpass);
mysql_select_db($sqldb);

?>
