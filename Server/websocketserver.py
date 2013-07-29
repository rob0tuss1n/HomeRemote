import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.template
import gui
import thread
import globals
from start import sensors, security, event, gpio

class WebSocket(tornado.websocket.WebSocketHandler):
    # Handle a new web client
    def open(self):
        globals.clients.append(self)
        gui.console("Websocket Opened")

    def on_message(self, message):
        gui.console(message)
        args = message.split(":")
        # Create a new output (pin, name)
        if args[0] == "newoutput":
            if args[1] in globals.outputs:
                self.write_message("error:GPIO already setup on pin " + args[1])
            else:
                globals.outputs[args[1]] = gpio(args[1], args[2], None, 'out')
                globals.cur.execute("""INSERT INTO outputs VALUES (NULL,%s,%s)""",(args[2],args[1]))
                globals.con.commit()
                for i in globals.clients:
                    i.write_message("addlight:"+args[1]+":"+args[2])

        # Get all outputs that are globals.currently on
        elif args[0] == "getoutputson":
            total = 0
            on = 0
            for i in globals.outputs:
                if globals.outputs[i].get_state() == 1:
                    on = on + 1
                else:
                    total = total + 1
            self.write_message("lightoverview:"+str(on)+":"+str(total))

        # Set the state of an output (pin, state)
        elif args[0] == "setoutputstate":
            if args[1] in globals.outputs:
                res = globals.outputs[args[1]].output(args[2])
                if res is True:
                    self.write_message("ok:")
                else:
                    self.write_message("error:" + str(res))
            else:
                self.write_message("error:Output does not exist on pin " + args[1])

        # Toggle a pin to the opposite state (pin)
        elif args[0] == "togglepin":
            if args[1] in globals.outputs:
                res = globals.outputs[args[1]].toggle()
            else:
                self.write_message("error:Output does not exist on pin " + args[1])

        # Report back the state of pins as if they changed state
        elif args[0] == "declarepins":
            for i in globals.outputs:
                gui.console(str(i)+" "+str(globals.outputs[i].input()))
                if globals.outputs[i].input() == 0:
                    if globals.outputs[i].mcp:
                        self.write_message("pinchange:mcp"+str(globals.outputs[i].pin)+":on")
                    else:
                        self.write_message("pinchange:"+str(globals.outputs[i].pin)+":on")
                elif globals.outputs[i].input() == 1:
                    if globals.outputs[i].mcp:
                        self.write_message("pinchange:mcp"+str(globals.outputs[i].pin)+":off")
                    else:
                        self.write_message("pinchange:"+str(globals.outputs[i].pin)+":off")
        
        # Report back the state of all events as if they changed state
        elif args[0] == "declareevents":
            for i in globals.events:
                if globals.events[i].event_process != None:
                    self.write_message("eventchange:"+str(globals.events[i].id)+":on")
                else:
                    self.write_message("eventchange:"+str(globals.events[i].id)+":off")
                    
        # Toggle the state of an event
        elif args[0] == "toggleevent":
            args[1] = int(args[1])
            if globals.events[args[1]].event_process != None:
                globals.events[args[1]].stop_event()
                for i in globals.clients:
                    i.write_message("eventchange:"+str(args[1])+":off")   
            else:
                globals.events[args[1]].start_event()
                for i in globals.clients:
                    i.write_message("eventchange:"+str(args[1])+":on")

        # Remove a light from the system
        elif args[0] == "deletelight":
            globals.cur.execute("""DELETE FROM outputs WHERE pin = %s""",(args[1]))
            globals.con.commit()
            del globals.outputs[args[1]]
            for i in globals.clients:
                i.write_message("deletelight:"+args[1])
            gui.remove_output(args[1])
                
        # Create a new event (name, 
        elif args[0] == "newevent":
            args[5] = args[5].replace("-", ":")
            globals.cur.execute("""INSERT INTO events VALUES (NULL,%s,%s,%s,%s,%s,%s)""",(args[1],args[2], args[3], args[4], args[5], args[6]))
            globals.con.commit()
            globals.cur.execute("SELECT `id`, `trigger` FROM events WHERE name = '"+args[1]+"'")
            eventdat = globals.cur.fetchone()
            globals.events[eventdat['id']] = event(eventdat['id'])
            
        # Remove an event from the system
        elif args[0] == "deleteevent":
            globals.events[int(args[1])].stop_event()
            del globals.events[int(args[1])]
            globals.cur.execute("""DELETE FROM events WHERE id = '%s'""",(int(args[1])))
            globals.con.commit()
            for i in globals.clients:
                i.write_message("deleteevent:"+args[1])
            gui.remove_event(args[1])
                
        # Create a new input (name, pin, type, )
        elif args[0] == "newinput":
            if args[1] in globals.inputs:
                self.write_message("error:Input already exists on pin "+args[2])
            else:
                globals.cur.execute("""INSERT INTO inputs VALUES (NULL,%s,%s,%s,%s)""",(args[1],args[2],args[3],args[4]))
                globals.con.commit()
                globals.inputs[args[2]] = gpio(args[2], args[1], args[3], "in")
                #events[int(args[2])] = event(0, True, args[2])
             
        # Remove an input from the system   
        elif args[0] == "deleteinput":
            globals.cur.execute("SELECT name FROM events WHERE `trigger` = "+args[1])
            if globals.cur.fetchone():
                self.write_message("error:Please delete the associated event for this input first!")
            else:
                globals.cur.execute("""DELETE FROM inputs WHERE pin = %s""",(int(args[1])))
                globals.con.commit()
                if globals.inputs[int(args[1])].in_type == "temp":
                    del globals.temp_sensors[globals.inputs[int(args[1])].name]
                    globals.sensors_index['temp'].remove(globals.inputs[int(args[1])].name)
                    del sensors.temp[globals.inputs[int(args[1])].name]
                elif globals.inputs[int(args[1])].in_type == "light":
                    del globals.light_sensors[globals.inputs[int(args[1])].name]
                    globals.sensors_index['light'].remove(globals.inputs[int(args[1])].name)
                elif globals.inputs[int(args[1])].in_type == "switch" or globals.inputs[int(args[1])].in_type == "motion":
                    globals.inputs[int(args[1])].stop_input_idle()
                del globals.inputs[int(args[1])]
                for i in globals.clients:
                    i.write_message("deleteinput:"+args[1])
                gui.remove_input(args[1])
                
        # Report back the globals.current state of the security system
        elif args[0] == "securitystatus":
            if security.armed_status:
                self.write_message("securitystatus:armed:"+security.mode)
            else:
                self.write_message("securitystatus:disarmed")
                
        # Arm the security system in mode (mode)
        elif args[0] == "armalarm":
            thread.start_new_thread(security.arm_system, (args[1],))
            for i in globals.clients:
                i.write_message("securitystatus:armed:"+args[1])
            
        elif args[0] == "disarmalarm":
            security.disarm_system()
            for i in globals.clients:
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
        globals.clients.remove(self)

def start_websocket_server():
    application = tornado.web.Application([(r"/", WebSocket),])
    application.listen(9000, '0.0.0.0')
    gui.console("Server started. Waiting for clients")
    tornado.ioloop.IOLoop.instance().start()
