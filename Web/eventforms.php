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
}