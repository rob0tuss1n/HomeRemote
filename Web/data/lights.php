<?php
require_once 'settings.php';

if(isset($_GET['action']) && $_GET['action'] == "getlights") {
    echo $GLOBALS['db']->sql_select("outputs");
}