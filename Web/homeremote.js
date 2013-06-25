var ws, page = $(location).attr('pathname'), color, remcolor, selector;
$(document).ready(function() {
    ws = new WebSocket('ws://192.168.1.68:9000/');
    ws.onopen = function() {
        ws.send("declarepins:");
        ws.send("declareevents:");
        ws.send("securitystatus:");
    };
    ws.onmessage = function(e) {
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
            if(args[1] == "armed") {
                $("#security-overview").html("System <b>armed</b> in "+args[2]+" mode");
            } else {
                $("#security-overview").html("System <b>disarmed</b>")
            }
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
                var html = '<tr class="light" data-pin="'+v['pin']+'"><td>'+ v.name+'</td><td><button type="submit" onclick="toggleLight('+"'"+ v.pin+"'"+')" class="small red"><span>Toggle</span></button></td><td><a href="#" onclick="deleteLight('+ v.pin+')"><img src="gfx/icon-delete.gif"></a></td></tr>';
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
        })
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
    var name = $("#new-input-name").val(), pin = $("#new-input-pin").val(), type = $("#new-input-type").val();
    ws.send("newinput:"+name+":"+pin+":"+type);
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