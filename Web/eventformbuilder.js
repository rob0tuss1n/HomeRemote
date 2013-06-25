function outputinputtimeout(initial) {
    var options = $("#event-options");
    options.html("");
    var lights = '<div class="row"><label for="who">Lights</label><div class="rowright"><select class="multiple" multiple="multiple" id="who"></select></div></div>';
    $(lights).appendTo(options);
    $.get("data/lights.php?action=getlights", function(data) {
        var lights = JSON.parse(data);
        $.each(lights, function(k, v) {
            $('<option value="'+ v.pin +'">'+ v.name +'</option>').appendTo("#who");
        })
    });

    $.get("eventforms.php?part=inputwhentarget", function(data) {
        $(data).appendTo(options);
        $("#trigger").selectBox();
        var timeout = '<div class="row"><label for="timeout">Timeout</label><div class="rowright"><input type="text" id="timeout"></div></div>';
        $(timeout).appendTo(options);
    });
}
function inputtoggleoutput() {
    var options = $("#event-options");
    options.html("");
    var lights = '<div class="row"><label for="who">Lights</label><div class="rowright"><select class="multiple" multiple="multiple" id="who"></select></div></div>';
    $(lights).appendTo(options);
    $.get("data/lights.php?action=getlights", function(data) {
        var lights = JSON.parse(data);
        $.each(lights, function(k, v) {
            $('<option value="'+ v.pin +'">'+ v.name +'</option>').appendTo("#who");
        })
    });

    $.get("eventforms.php?part=inputwhentarget", function(data) {
        $(data).appendTo(options);
        $("#trigger").selectBox();
    });
}
function outputtime() {
    var options = $("#event-options");
    options.html("");
    var lights = '<div class="row"><label for="who">Lights</label><div class="rowright"><select class="multiple" multiple="multiple" id="who"></select></div></div>';
    $(lights).appendTo(options);
    $.get("data/lights.php?action=getlights", function(data) {
        var lights = JSON.parse(data);
        $.each(lights, function(k, v) {
            $('<option value="'+ v.pin +'">'+ v.name +'</option>').appendTo("#who");
        })
    });
    $('<input type="hidden" id="trigger" value="time">').appendTo(options);

    var time = '<div class="row"><label for="time-hour">Time</label><div class="rowright"><select id="time-hour"><option selected="selected" value="01">1</option><option value="02">2</option><option value="03">3</option><option value="04">4</option><option value="05">5</option><option value="06">6</option><option value="07">7</option><option value="08">8</option><option value="09">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option></select><select id="time-minute"><option selected="selected" value="00">00</option><option value="01">01</option><option value="02">02</option><option value="03">03</option><option value="04">04</option><option value="05">05</option><option value="06">06</option><option value="07">07</option><option value="08">08</option><option value="09">09</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option><option value="23">23</option><option value="24">24</option><option value="25">25</option><option value="26">26</option><option value="27">27</option><option value="28">28</option><option value="29">29</option><option value="30">30</option><option value="31">31</option><option value="32">32</option><option value="33">33</option><option value="34">34</option><option value="35">35</option><option value="36">36</option><option value="37">37</option><option value="38">38</option><option value="39">39</option><option value="40">40</option><option value="41">41</option><option value="42">42</option><option value="43">43</option><option value="44">44</option><option value="45">45</option><option value="46">46</option><option value="47">47</option><option value="48">48</option><option value="49">49</option><option value="50">50</option><option value="51">51</option><option value="52">52</option><option value="53">53</option><option value="54">54</option><option value="55">55</option><option value="56">56</option><option value="12">57</option><option value="12">58</option><option value="12">59</option></select><select id="time-day"><option selected="selected" value="AM">AM</option><option selected="selected" value="PM">PM</option></select></div></div>';
    $(time).appendTo(options);
    $("#time-hour").selectBox();
    $("#time-minute").selectBox();
    $("#time-day").selectBox();
}
function eventtime() {
    var options = $("#event-options");
    options.html("");
    var lights = '<div class="row"><label for="who">Events</label><div class="rowright"><select id="who"></select></div></div>';
    $(lights).appendTo(options);
    $.get("data/events.php?action=getevents", function(data) {
        var lights = JSON.parse(data);
        $.each(lights, function(k, v) {
            $('<option value="'+ v.id +'">'+ v.name +'</option>').appendTo("#who");
        });
        $("#who").selectBox();
    });

    $('<input type="hidden" id="trigger" value="time')
    var time = '<div class="row"><label for="time-hour">Time</label><div class="rowright"><select id="time-hour"><option selected="selected" value="01">1</option><option value="02">2</option><option value="03">3</option><option value="04">4</option><option value="05">5</option><option value="06">6</option><option value="07">7</option><option value="08">8</option><option value="09">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option></select><select id="time-minute"><option selected="selected" value="00">00</option><option value="01">01</option><option value="02">02</option><option value="03">03</option><option value="04">04</option><option value="05">05</option><option value="06">06</option><option value="07">07</option><option value="08">08</option><option value="09">09</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option><option value="23">23</option><option value="24">24</option><option value="25">25</option><option value="26">26</option><option value="27">27</option><option value="28">28</option><option value="29">29</option><option value="30">30</option><option value="31">31</option><option value="32">32</option><option value="33">33</option><option value="34">34</option><option value="35">35</option><option value="36">36</option><option value="37">37</option><option value="38">38</option><option value="39">39</option><option value="40">40</option><option value="41">41</option><option value="42">42</option><option value="43">43</option><option value="44">44</option><option value="45">45</option><option value="46">46</option><option value="47">47</option><option value="48">48</option><option value="49">49</option><option value="50">50</option><option value="51">51</option><option value="52">52</option><option value="53">53</option><option value="54">54</option><option value="55">55</option><option value="56">56</option><option value="12">57</option><option value="12">58</option><option value="12">59</option></select><select id="time-day"><option selected="selected" value="AM">AM</option><option selected="selected" value="PM">PM</option></select></div></div>';
    $(time).appendTo(options);
    $("#time-hour").selectBox();
    $("#time-minute").selectBox();
    $("#time-day").selectBox();
}
function eventinput() {
    var options = $("#event-options");
    options.html("");
    var lights = '<div class="row"><label for="who">Event</label><div class="rowright"><select id="who"></select></div></div>';
    $(lights).appendTo(options);
    $.get("data/events.php?action=getevents", function(data) {
        var lights = JSON.parse(data);
        $.each(lights, function(k, v) {
            $('<option value="'+ v.pin +'">'+ v.name +'</option>').appendTo("#who");
        })
        $("#who").selectBox();
    });

    $.get("eventforms.php?part=inputwhentarget", function(data) {
        $(data).appendTo(options);
        $("#trigger").selectBox();
    });
}