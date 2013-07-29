var ws, args, page = $(location).attr('pathname'), color, remcolor, selector, url = $(location).attr("host");
$.get("data/auth.php?action=checkauth", function(data) {
    if(data == "false") {
        window.location.replace = url;
    } else {
        $("#user-name").html("Welcome, "+data);
    }
});
$(document).ready(function() {
    ws = new WebSocket('ws://joey.myds.me:9000/');
    ws.onopen = function() {
        ws.send("declarepins:");
        ws.send("declareevents:");
        ws.send("securitystatus:");
        ws.send("gettemp:");
    };
    ws.onmessage = function(e) {
        console.log(e.data)
        args = e.data.split(":");
        if(args[0] == "error") {
            alert("Error: "+args[1]);
        } else if(args[0] == "pinchange") {
            if(args[2] == "on") {
                color = "green";
                remcolor = "red";
            } else {
                color = "red";
                remcolor = "green";
            }
            selector = $("tr[data-pin='"+args[1]+"']");
            selector.find("button").removeClass(remcolor);
            selector.find("button").addClass(color);
        } else if(args[0] == "eventchange") {
            if(args[2] == "on") {
                color = "green";
                remcolor = "red";
            } else {
                color = "red";
                remcolor = "green";
            }
            selector = $("tr[data-eventid='"+args[1]+"']");
            selector.find("button").removeClass(remcolor);
            selector.find("button").addClass(color);
        }  else if(args[0] == "inputchange") {
            if(args[2] == "on") {
                color = "green";
                remcolor = "red";
            } else {
                color = "red";
                remcolor = "green";
            }
            selector = $("tr[data-inputpin='"+args[1]+"']");
            selector.find("button").removeClass(remcolor);
            selector.find("button").addClass(color);
        } else if(args[0] == "securitystatus") {
            var selector = $("#security-overview")
            if(args[1] == "armed") {
                selector.html("System <b>armed</b> in "+args[2]+" mode");
            } else {
                selector.html("System <b>disarmed</b>")
            }
            $.get("data/system.php?action=getmotionstatus", function(data) {
                selector.html(selector.html()+", "+data);
            });
        }
        if(args[0] == "deletelight") {
            $("tr[data-pin='"+args[1]+"']").remove();
        } else if(args[0] == "addlight") {
            console.log(e.data);
            var html = '<tr class="light" data-pin="'+args[1]+'"><td>'+args[2]+'</td><td><button type="submit" onclick="toggleLight('+"'"+args[1]+"'"+')" class="small red"><span>Toggle</span></button></td><td><a href="#" onclick="deleteLight('+args[1]+')"><img src="gfx/icon-delete.gif"></a></td></tr>';
            $(html).appendTo($("#lightlist"));
        } else if(args[0] == "deleteevent") {
            $("tr[data-eventid='"+args[1]+"']").remove();
        } else if(args[0] == "deleteinput") {
            $("tr[data-inputpin='"+args[1]+"']").remove();
        } else if(args[0] == "alarmtrip") {
            alert("BURGLER ALARM HAS BEEN TRIPPED!");
        } else if(args[0] == "refreshpage") {
            location.reload();
        } else if(args[0] == "temperature") {
            $("#indoor-temp").html(args[1]+"&deg; F");
        } else if(args[0] == "lightlevel") {
            console.log("Light level: "+args[1])
        }
    };
    if(page == "/dashboard.html") {
        $.get("data/lights.php?action=getlights", function(data) {
            lights = JSON.parse(data);
            $.each(lights, function(k, v) {
                var html = '<tr class="light" data-pin="'+v['pin']+'"><td>'+v['name']+'</td><td><button type="submit" onclick="toggleLight('+"'"+v['pin']+"'"+')" class="small red"><span>Toggle</span></button></td></tr>';
                $(html).appendTo($("#lightlist"));
            });
        });
        $.get("data/events.php?action=getevents", function(data) {
            events = JSON.parse(data);
            $.each(events, function(k, v) {
                var html = '<tr class="event" data-eventid="'+v['id']+'"><td>'+v['name']+'</td><td><button type="submit" onclick="toggleEvent('+v['id']+')" class="small red"><span>Toggle</span></button></td></tr>';
                $(html).appendTo($("#eventlist"));
            });
        });
        $.get("data/weather.php?action=getweather", function(data) {
            weather = JSON.parse(data);
            $("#outdoor-temp").html(weather.main.temp+"&deg; F");
        });
        $.get("data/system.php?action=gettime", function(data) {
            $("#time").html(data);
        });
    } else if(page == "/lights.html") {
        $.get("data/lights.php?action=getlights", function(data) {
            lights = JSON.parse(data);
            $.each(lights, function(k, v) {
                var html = '<tr class="light" data-pin="'+v['pin']+'"><td>'+ v.name+'</td><td><button type="submit" onclick="toggleLight('+"'"+ v.pin+"'"+')" class="small red"><span>Toggle</span></button></td><td><a href="#" onclick="deleteLight('+"'"+ v.pin+"'"+')"><img src="gfx/icon-delete.gif"></a></td></tr>';
                $(html).appendTo($("#lightlist"));
            });
        });
    } else if(page == "/events.html") {
        $.get("data/events.php?action=getevents", function(data) {
            var events = JSON.parse(data);
            $.each(events, function(k, v) {
                var html = '<tr class="event" data-eventid="'+ v.id+'"><td>'+ v.name+'</td><td><button type="submit" onclick="toggleEvent('+ v.id+')" class="small red"><span>Toggle</span></button></td><td><a href="#" onclick="deleteEvent('+ v.id+')"><img src="gfx/icon-delete.gif"></a></td></tr>';
                $(html).appendTo($("#eventlist"));
            });
        });

        outputinputtimeout(true);
        $("#event-type").selectBox().change(function() {
            if($(this).val() == "output_toggle_on_input_timeout") {
                outputinputtimeout(false);
            } else if($(this).val()=="output_toggle_on_input") {
                inputtoggleoutput();
            } else if($(this).val()=="output_off_on_input") {
                inputtoggleoutput();
            } else if($(this).val()=="output_on_on_input") {
                inputtoggleoutput();
            } else if($(this).val()=="output_on_at_time") {
                outputtime();
            } else if($(this).val()=="output_off_at_time") {
                outputtime();
            } else if($(this).val()=="event_enable_on_input") {
                eventinput();
            } else if($(this).val()=="event_disable_on_input") {
                eventinput();
            } else if($(this).val()=="event_enable_at_time") {
                eventtime();
            } else if($(this).val()=="event_disable_at_time") {
                eventtime();
            }
        });
    } else if(page == "/inputs.html") {
        $.get("data/inputs.php?action=getinputs", function(data) {
            inputs = JSON.parse(data);
            $.each(inputs, function(k, v) {
                var html = '<tr class="input" data-inputpin="'+ v.pin+'"><td>'+ v.name+'</td><td><button class="small red"><span>Status</span></button></td><td><a href="#" onclick="deleteInput('+ v.pin+')"><img src="gfx/icon-delete.gif"></a></td></tr>';
                $(html).appendTo($("#inputlist"));
            })
        });
        $("#new-input-type").selectBox().change(function() {
            if($(this).val() == "temp") {
                $("#input-type-row").after($('<div id="temp-type" class="row"><label>Light sensor type</label><div class="rowright"><select id="light-sensor-type"><option value="11">DHT11</option><option value="22">DHT22</option><option value="2302">AM2302</option></select></div></div>'));
                $("#light-sensor-type").selectBox();
            } else {
                $("#temp-type").remove();
            }
        })
    } else if(page == "/security.html") {
        $.get("data/security.php?action=getcamerafeeds", function(data) {
            feeds = JSON.parse(data);
            $.each(feeds, function(k, v) {
                var html = '<div onclick="imageviewer('+"'"+ v.name +"'"+')" class="camera-feed" style="width: 640px; height: 500px; text-align: center;"><span style="text-align: center; cursor: pointer;"><b>'+ v.name +'</b></span><br><iframe style="border: none;" src="http://'+ v.server_address +'" width="640" height="480"></iframe></div>';
                $(html).appendTo($("#camerafeeds"));
            })
        });
        $.get("eventforms.php?part=zone", function(data) {
            $(data).appendTo($("#new-zone-form"));
            $("#camera").selectBox();
            $("#input").selectBox();
        });
    } else if(page == "/temperature.html") {
        $.get("data/temperature.php?action=get24hdata", function(data) {
            temps = JSON.parse(data);
            $.each(temps, function(k,v) {
                var html = '<tr><th>'+ v.date +'</th><td>'+ v.temp +'</td></tr>'
                $(html).appendTo($("#temp-history-data"));
            });
        });
    }
});

function toggleLight(pin) {
    ws.send("togglepin:"+pin);
}
function toggleEvent(id) {
    ws.send("toggleevent:"+id);
}
function deleteLight(pin) {
    ws.send("deletelight:"+pin);
}
function addLight() {
    var name = $("#new-light-name").val(), pin = $("#new-light-pin").val();
    ws.send("newoutput:"+pin+":"+name);
}
function addEvent() {
    var name = $("#new-event-name").val(), action = $("#event-type").val(), who = $("#who").val(), timeout = $("#timeout").val(), trigger = $("#trigger").val(), trigger_args;
    if(trigger == "time") {
        trigger_args = $("#time-hour").val()+"-"+$("#time-minute").val()+" "+$("#time-day").val();
    }
    ws.send("newevent:"+name+":"+action+":"+who+":"+trigger+":"+trigger_args+":"+timeout)
}
function deleteEvent(id) {
    ws.send("deleteevent:"+id);
}
function addInput() {
    var name = $("#new-input-name").val(), pin = $("#new-input-pin").val(), type = $("#new-input-type").val(), type_args;
    if(type == "temp") {
        type_args = $("#light-sensor-type").val();
    }
    ws.send("newinput:"+name+":"+pin+":"+type+":"+type_args);
}
function deleteInput(pin) {
    ws.send("deleteinput:"+pin);
}
function armAway() {
    if (confirm('Are you sure you want to arm the security system in AWAY mode?')) {
        ws.send("armalarm:away");
    }
}
function armNight() {
    if (confirm('Are you sure you want to arm the security system in NIGHT mode?')) {
        ws.send("armalarm:night")
    }
}
function disarm() {
    ws.send("disarmalarm:");
}
function reloadCam(element, img) {

}