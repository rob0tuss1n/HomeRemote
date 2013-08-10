<?php
require_once 'settings.php';

if(isset($_GET['action']) && $_GET['action'] == "getinputs") {
    echo $GLOBALS['db']->sql_select("inputs");
}