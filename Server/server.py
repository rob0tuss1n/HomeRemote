import sys
import os
try:
   with open('lock.pid'): pass
   print 'Lock file already exists! This probably means HomeRemote is already running or that it was improperly shutdown (crash)\n Delete the lockfile at /etc/remotehome/lock.pid and try again!'
   sys.exit()
except IOError:
    with open('lock.pid', 'w') as lockfile:
        os.chmod("/etc/homeremote/lock.pid", 0666)
        lockfile.write(str(os.getpid()))
        lockfile.close()
import RPi.GPIO as GPIO
from mcp import MCP230XX_GPIO as mcp
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.template
import gui
import signal
import thread
from remotehome import clients, event, events, inputs, outputs, gpio, security, cur, con, sensors, sensors_index, nogui, temp_sensors, light_sensors

security = security()
daemonize = False
for i in sys.argv:
    if i == "-nogui":
        nogui = True
    if i == "-D":
        daemonize = True
        nogui = True

if not nogui:
    gui.start()
if daemonize:
    gui.no_output = True

if __name__ == "__main__":
    # Get pins and set them up
    cur.execute("SELECT name, pin FROM outputs")
    data = cur.fetchall()
    for i in data:
        outputs[str(i['pin'])] = gpio(i['pin'], i['name'], "none", 'out')
        
    # Get inputs and set them up
    cur.execute("SELECT name, pin, type FROM inputs")
    data = cur.fetchall()
    for i in data:
        inputs[int(i['pin'])] = gpio(i['pin'], i['name'], i['type'], 'in')
    
    # Get events and set them up
    cur.execute("SELECT id FROM events")
    eventsdata = cur.fetchall()
    for i in eventsdata:
        events[int(i['id'])] = event(int(i['id']), cur)

sensors = sensors()

class WebSocket(tornado.websocket.WebSocketHandler):
    # Handle a new web client
    def open(self):
        clients.append(self)
        gui.console("Websocket Opened")

    def on_message(self, message):
        gui.console(message)
        args = message.split(":")
        # Create a new output (pin, name)
        if args[0] == "newoutput":
            if args[1] in outputs:
                self.write_message("error:GPIO already setup on pin " + args[1])
            else:
                outputs[args[1]] = gpio(args[1], args[2], None, 'out')
                cur.execute("""INSERT INTO outputs VALUES (NULL,%s,%s)""",(args[2],args[1]))
                con.commit()
                for i in clients:
                    i.write_message("addlight:"+args[1]+":"+args[2])

        # Get all outputs that are currently on
        elif args[0] == "getoutputson":
            total = 0
            on = 0
            for i in outputs:
                if outputs[i].get_state() == 1:
                    on = on + 1
                else:
                    total = total + 1
            self.write_message("lightoverview:"+str(on)+":"+str(total))

        # Set the state of an output (pin, state)
        elif args[0] == "setoutputstate":
            if args[1] in outputs:
                res = outputs[args[1]].output(args[2])
                if res is True:
                    self.write_message("ok:")
                else:
                    self.write_message("error:" + str(res))
            else:
                self.write_message("error:Output does not exist on pin " + args[1])

        # Toggle a pin to the opposite state (pin)
        elif args[0] == "togglepin":
            if args[1] in outputs:
                res = outputs[args[1]].toggle()
            else:
                self.write_message("error:Output does not exist on pin " + args[1])

        # Report back the state of pins as if they changed state
        elif args[0] == "declarepins":
            for i in outputs:
                gui.console(str(i)+" "+str(outputs[i].input()))
                if outputs[i].input() == 0:
                    if outputs[i].mcp:
                        self.write_message("pinchange:mcp"+str(outputs[i].pin)+":on")
                    else:
                        self.write_message("pinchange:"+str(outputs[i].pin)+":on")
                elif outputs[i].input() == 1:
                    if outputs[i].mcp:
                        self.write_message("pinchange:mcp"+str(outputs[i].pin)+":off")
                    else:
                        self.write_message("pinchange:"+str(outputs[i].pin)+":off")
        
        # Report back the state of all events as if they changed state
        elif args[0] == "declareevents":
            for i in events:
                if events[i].event_process != None:
                    self.write_message("eventchange:"+str(events[i].id)+":on")
                else:
                    self.write_message("eventchange:"+str(events[i].id)+":off")
                    
        # Toggle the state of an event
        elif args[0] == "toggleevent":
            args[1] = int(args[1])
            if events[args[1]].event_process != None:
                events[args[1]].stop_event()
                for i in clients:
                    i.write_message("eventchange:"+str(args[1])+":off")   
            else:
                events[args[1]].start_event()
                for i in clients:
                    i.write_message("eventchange:"+str(args[1])+":on")

        # Remove a light from the system
        elif args[0] == "deletelight":
            cur.execute("""DELETE FROM outputs WHERE pin = %s""",(args[1]))
            con.commit()
            del outputs[args[1]]
            for i in clients:
                i.write_message("deletelight:"+args[1])
            gui.remove_output(args[1])
                
        # Create a new event (name, 
        elif args[0] == "newevent":
            args[5] = args[5].replace("-", ":")
            cur.execute("""INSERT INTO events VALUES (NULL,%s,%s,%s,%s,%s,%s)""",(args[1],args[2], args[3], args[4], args[5], args[6]))
            con.commit()
            cur.execute("SELECT `id`, `trigger` FROM events WHERE name = '"+args[1]+"'")
            eventdat = cur.fetchone()
            events[eventdat['id']] = event(eventdat['id'], cur)
            
        # Remove an event from the system
        elif args[0] == "deleteevent":
            events[int(args[1])].stop_event()
            del events[int(args[1])]
            cur.execute("""DELETE FROM events WHERE id = '%s'""",(int(args[1])))
            con.commit()
            for i in clients:
                i.write_message("deleteevent:"+args[1])
            gui.remove_event(args[1])
                
        # Create a new input (name, pin, type, )
        elif args[0] == "newinput":
            if args[1] in inputs:
                self.write_message("error:Input already exists on pin "+args[2])
            else:
                cur.execute("""INSERT INTO inputs VALUES (NULL,%s,%s,%s,%s)""",(args[1],args[2],args[3],args[4]))
                con.commit()
                inputs[args[2]] = gpio(args[2], args[1], args[3], "in")
                #events[int(args[2])] = event(0, True, args[2])
             
        # Remove an input from the system   
        elif args[0] == "deleteinput":
            cur.execute("SELECT name FROM events WHERE `trigger` = "+args[1])
            if cur.fetchone():
                self.write_message("error:Please delete the associated event for this input first!")
            else:
                cur.execute("""DELETE FROM inputs WHERE pin = %s""",(int(args[1])))
                con.commit()
                if inputs[int(args[1])].in_type == "temp":
                    del temp_sensors[inputs[int(args[1])].name]
                    sensors_index['temp'].remove(inputs[int(args[1])].name)
                    del sensors.temp[inputs[int(args[1])].name]
                elif inputs[int(args[1])].in_type == "light":
                    del light_sensors[inputs[int(args[1])].name]
                    sensors_index['light'].remove(inputs[int(args[1])].name)
                elif inputs[int(args[1])].in_type == "switch" or inputs[int(args[1])].in_type == "motion":
                    inputs[int(args[1])].stop_input_idle()
                del inputs[int(args[1])]
                for i in clients:
                    i.write_message("deleteinput:"+args[1])
                gui.remove_input(args[1])
                
        # Report back the current state of the security system
        elif args[0] == "securitystatus":
            if security.armed_status:
                self.write_message("securitystatus:armed:"+security.mode)
            else:
                self.write_message("securitystatus:disarmed")
                
        # Arm the security system in mode (mode)
        elif args[0] == "armalarm":
            thread.start_new_thread(security.arm_system, (args[1],))
            for i in clients:
                i.write_message("securitystatus:armed:"+args[1])
            
        elif args[0] == "disarmalarm":
            security.disarm_system()
            for i in clients:
                i.write_message("securitystatus:disarmed")
        elif args[0] == "addcamera":
            security.addcamera(args[1],args[2], args[3], args[4], args[5])
        elif args[0] == "removecamera":
            security.removecamera(args[1])
        elif args[0] == "gettemp":
            self.write_message("temperature:"+sensors.get_temperature())
        elif args[0] == "gethumid":
            self.write_message("humidity:"+sensors.get_humidity())
        elif args[0] == "getlightlevel":
            self.write_message("lightlevel:"+sensors.get_light_level())
                
    def on_close(self):
        gui.console("Websocket closed")
        clients.remove(self)

application = tornado.web.Application([(r"/", WebSocket),])
def signal_handler(signal, frame):
        # Run all clean-up functions to indicate a safe shutdown
        gui.console('Closing server')
        for i in clients:
            i.close()
        for i in events:
            events[i].stop_event()
        for i in inputs:
            if inputs[i].idling:
                inputs[i].stop_input_idle()
        sensors.temp_process.terminate()
        sensors.run_sensor_refresh = False
        GPIO.cleanup()
        gui.end()
        os.remove('lock.pid')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    application.listen(9000, '0.0.0.0')
    gui.console("Server started. Waiting for clients")
    tornado.ioloop.IOLoop.instance().start()
