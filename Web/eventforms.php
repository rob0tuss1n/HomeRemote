<?php
if($_GET['part'] == "inputwhentarget") {
    echo '
    <div class="row">
        <label for="trigger">Input</label>
        <div class="rowright">
            <select id="trigger">';
                require_once 'data/inputs.php';
                $lights = json_decode(getInputs());
                foreach($lights as $light) {
                    $light = (array) $light;
                    echo '<option value="'.$light['pin'].'">'.$light['name'].'</option>';
                }
            echo '</select>
        </div>
    </div>';
} elseif($_GET['part'] == "zone") {
    echo '
    <div class="row">
        <label for="input">Zone Input</label>
        <div class="rowright">
            <select id="input">';
    require_once 'data/inputs.php';
    $inputs = json_decode(getInputs());
    foreach($inputs as $input) {
        $input = (array) $input;
        echo '<option value="'.$input['pin'].'">'.$input['name'].'</option>';
    }
    echo '</select>
        </div>
    </div>';
    echo '
    <div class="row">
        <label for="camera">Camera</label>
        <div class="rowright">
            <select id="camera">';
    require_once 'data/security.php';
    $feeds = json_decode(getUnusedCams());
    $dirs = scandir("/dev");
    foreach($dirs as $dir) {
        if(strstr($dir, "video")) {
            if(in_array($dir, $feeds)) {
                echo '<option value="'.$dir.'">'.$dir.'</option>';
                $gotone = true;
            }
        }
    }
    if(@!$gotone) {
        echo '<option value="none">No video inputs avaliabe</option>';
    }
    echo '</select>
        </div>
    </div>';
    echo '
    <div class="row">
                                <div class="rowright">
                                    <button class="medium" onclick="addZone()"><span>Add</span></button>
                                </div>
                            </div>';
}