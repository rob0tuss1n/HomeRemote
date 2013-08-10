import RPi.GPIO as GPIO
import sqlite3
from multiprocessing import Process, Pipe
import thread
from threading import Thread
import time
import gui
import re
import extender
import subprocess
import os
import psutil
import globals

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class event(object):
    id = None
    trigger = None
    action = None
    trigger_arg = None
    action_arg = None
    who = None
    cur = None
    pipe_thread = None
    parent_conn, child_conn = Pipe()
    keep_piping = True
    event_process = None
    has_input = False
    events = None
    first_start = True
    
    def __init__(self, id):
        self.pipe_thread = Thread(target=self.pipe_listen, args=())
        self.id = id
        globals.cur.execute('SELECT * FROM events WHERE id = %s' % (self.id))
        data = globals.cur.fetchone()
        self.name = data['name']
        self.trigger = int(data['trigger'])
        self.trigger_args = data['trigger_args']
        self.action = data['action']
        self.who = data['who'].split(",")
        try:
            self.timeout = int(data['timeout'])
        except:
            pass
        gui.add_event(self.name, self.id)
        self.start_event()
            
    def pipe_listen(self):
        while self.keep_piping:
            if self.parent_conn.poll():
                msg = self.parent_conn.recv()
                data = msg.split(":")
                if data[0] == "eventchange":
                    if data[2] == "on":
                        globals.events[data[1]].start_event()
                    elif data[2] == "off":
                        globals.events[data[1]].stop_event()
                for i in globals.clients:
                    i.write_message(msg)
            time.sleep(0.1)
        self.parent_conn.close()
        
    def start_event(self):
        self.parent_conn, self.child_conn = Pipe()
        self.keep_piping = True
        self.pipe_thread = Thread(target=self.pipe_listen, args=())
        self.pipe_thread.start()
        self.run_event()
        
    def stop_event(self):
        if self.event_process != None:
            globals.cur.execute('DELETE FROM helper_processes WHERE pid = %s' % (self.event_process.pid))
            globals.con.commit()
            self.event_process.terminate()
            self.event_process = None
        gui.change_event_state(self.id, 0)
        self.keep_piping = False
        if self.has_input:
            globals.inputs[self.trigger].start_input_idle()
            
    def run_event(self):
        if self.action == "output_toggle_on_input_timeout":
            self.event_process = Process(target=self.output_toggle_on_input_timeout, args=(self.child_conn,))
            self.has_input = True
            globals.inputs[self.trigger].event_id = self.id
            globals.inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_toggle_on_input":
            self.event_process = Process(target=self.output_toggle_on_input, args=(self.child_conn,))
            self.has_input = True
            globals.inputs[self.trigger].event_id = self.id
            globals.inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_off_on_input":
            self.event_process = Process(target=self.output_off_on_input, args=(self.child_conn,))
            self.has_input = True
            globals.inputs[self.trigger].event_id = self.id
            globals.inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_on_on_input":
            self.event_process = Process(target=self.output_on_on_input, args=(self.child_conn,))
            self.has_input = True
            globals.inputs[self.trigger].event_id = self.id
            globals.inputs[self.trigger].stop_input_idle()
            
        elif self.action == "event_disable_on_input":
            self.event_process = Process(target=self.event_disable_on_input, args=(self.child_conn,))
            self.has_input = True
            globals.inputs[self.trigger].event_id = self.id
            globals.inputs[self.trigger].stop_input_idle()
            
        elif self.action == "event_enable_on_input":
            self.event_process = Process(target=self.event_enable_on_input, args=(self.child_conn,))
            self.has_input = True
            globals.inputs[self.trigger].event_id = self.id
            globals.inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_on_at_time":
            self.event_process = Process(target=self.output_on_at_time, args=(self.child_conn,))
        elif self.action == "output_off_at_time":
            self.event_process = Process(target=self.output_off_at_time, args=(self.child_conn,))
        elif self.action == "event_enable_at_time":
            self.event_process = Process(target=self.event_enable_at_time, args=(self.child_conn,))
        elif self.action == "event_disable_at_time":
            self.event_process = Process(target=self.event_disable_at_time, args=(self.child_conn,))
        time.sleep(1)
        self.event_process.start()
        globals.cur.execute('INSERT INTO helper_processes VALUES (%s,"%s",%s)' % (self.event_process.pid, "event", self.id))
        globals.con.commit()
        gui.change_event_state(self.id, 1)
        
    def idle_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.BOTH)
            conn.send("inputchange:"+str(self.trigger)+":on")
            gui.change_input_state(str(self.trigger), 1, "reg")
            GPIO.wait_for_edge(int(self.trigger), GPIO.BOTH)
            conn.send("inputchange:"+str(self.trigger)+":off")
            gui.change_input_state(self.trigger, 0, "reg")

    def output_toggle_on_input_timeout(self, conn):
        while True:
            alreadyon = []
            GPIO.wait_for_edge(int(self.trigger), GPIO.BOTH)
            conn.send("inputchange:"+str(self.trigger)+":on")
            gui.change_input_state(int(self.trigger), 1, "reg")
            for i in self.who:
                if globals.outputs[i].input() == 1:
                    alreadyon.append(i)
                    gui.console("Pin already on")
                else:
                    globals.outputs[i].output(1)
                    gui.change_output_state(i, 1)
                    conn.send("pinchange:"+i+":on")
            targettime = int(time.time()) + int(self.timeout)
            changed = False
            while not targettime == int(time.time()):
                if globals.inputs[int(self.trigger)].input():
                    if changed:
                        conn.send("inputchange:"+str(self.trigger)+":on")
                        gui.change_input_state(int(self.trigger), 1, "reg")
                        changed = False
                    targettime = int(time.time()) + self.timeout - 3
                else:
                    changed = True
                    conn.send("inputchange:"+str(self.trigger)+":off")
                    gui.change_input_state(int(self.trigger), 0, "reg")
                time.sleep(0.2)
            for i in self.who:
                if not i in alreadyon:
                    globals.outputs[i].output(0)
                    conn.send("pinchange:"+i+":off")
                    gui.change_output_state(i, 0)

    # Toggles all pins to same state first of which was not the previous state in this function
    def output_toggle_on_input(self, conn):
        state = 0
        while True:
            alreadyon = []
            GPIO.wait_for_edge(self.trigger, GPIO.RISING)
            conn.send("inputchange:"+str(self.trigger)+":on")
            gui.change_input_state(self.trigger, 1, "reg")
            for i in self.who:
                globals.outputs[i].output(state)
                gui.change_output_state(i, not state)
                if state == 0:
                    state = 1
                else:
                    state = 0
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            gui.change_input_state(self.trigger, 0, "reg")

    def output_off_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1, "reg")
            for i in self.who:
                globals.outputs[i].output(1)
                gui.change_output_state(i, 0)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_input_state(self.trigger, 0, "reg")

    def output_on_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1, "reg")
            for i in self.who:
                globals.outputs[i].output(0)
                gui.change_output_state(i, 1)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_input_state(self.trigger, 0, "reg")
            gui.change_output_state(self.trigger, 0)

    def event_enable_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1, "reg")
            conn.send("eventchange:"+self.who+":enable")
            gui.change_event_state(self.who, 1)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_input_state(self.trigger, 0, "reg")
            gui.change_event_state(self.trigger, 0)

    def event_disable_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1, "reg")
            conn.send("eventchange:"+self.who+":disable")
            gui.change_event_state(self.who, 0)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_input_state(self.trigger, 0, "reg")

    def output_on_at_time(self, conn):
        while True:
            nowtime = time.strftime("%I:%M %p", time.localtime())
            if self.trigger == nowtime:
                for i in self.who:
                    globals.outputs[i].output(0)
                    gui.change_output_state(i, 1)
            time.sleep(60)

    def output_off_at_time(self, conn):
        while True:
            nowtime = time.strftime("%I:%M %p", time.localtime())
            if self.trigger == nowtime:
                for i in self.who:
                    globals.outputs[i].output(1)
                    gui.change_output_state(i, 0)
            time.sleep(60)

    def event_enable_at_time(self, conn):
        while True:
            nowtime = time.strftime("%I:%M %p", time.localtime())
            if self.trigger == nowtime:
                conn.send("eventchange:"+self.who+":enable")
                gui.change_event_state(self.who, 1)
            time.sleep(60)

    def event_disable_at_time(self, conn):
        while True:
            nowtime = time.strftime("%I:%M %p", time.localtime())
            if self.trigger == nowtime:
                conn.send("eventchange:"+self.who+":disable")
                gui.change_event_state(self.who, 0)
            time.sleep(60)


class gpio(object):
    pin = None
    name = None
    direction = None
    used = False
    keep_piping = True
    manual_on = False
    event_id = None
    idling = False
    mcp = False
    in_type = None

    def __init__(self, pin, name, in_type, direction):
        self.name = name
        self.direction = direction
        if(direction == "out"):
            if "mcp" in pin:
                if not globals.mcp_loaded:
                    globals.mcp = extender.Adafruit_MCP230XX(busnum=1, address=0x20, num_gpios=16)
                    globals.mcp_loaded = True
                gui.console("Setting up MCP23017 pin")
                self.mcp = True
                self.pin = int(pin[3:])
                globals.mcp.config(self.pin, globals.mcp.OUTPUT)
            else:
                self.pin = int(pin)
                GPIO.setup(int(pin), GPIO.OUT)
            gui.add_output(name, pin)
            #thread.start_new_thread(self.identify, ())
        elif direction == "in":
            self.pin = int(pin)
            self.in_type = in_type
            if in_type == "switch":
                GPIO.setup(int(pin), GPIO.IN, pull_up_down=GPIO.PUD_UP)
                self.start_input_idle()
                gui.add_input(name, pin, "reg")
            elif in_type == "motion":
                GPIO.setup(int(pin), GPIO.IN)
                self.start_input_idle()
                gui.add_input(name, pin, "reg")
            elif in_type == "temp":
                globals.sensors_index['temp'].append(str(self.name))
                globals.temp_sensors[self.name] = str(self.pin)
                gui.add_input(name, pin, "temp")
            elif in_type == "light":
                globals.sensors_index['light'].append(str(self.name))
                globals.light_sensors[self.name] = str(self.pin)
                gui.add_input(name, pin, "light")
            else:
                gui.console("Failed to setup GPIO: Unknown input type for pin "+str(self.pin))
                return
        else:
            gui.console("Failed to setup GPIO: Unrecognized direction!")
            return
        gui.console("Setup new GPIO. Pin: " + str(pin) + ", Name: " + name + ", Direction: " + direction)

    def input(self):
        if self.mcp and self.direction == "out":
            return int(globals.mcp.input(self.pin, check=False))
        elif self.direction == "out" and not self.mcp:
            return GPIO.input(self.pin)
        else:
            return GPIO.input(self.pin)

    def output(self, value):
        if self.mcp:
            gui.change_output_state("mcp"+str(self.pin), int(value))
            globals.mcp.output(self.pin, int(value))
            if int(value) == 1:
                for i in globals.clients:
                    i.write_message("pinchange:mcp"+str(self.pin)+":on")
            elif int(value) == 0:
                for i in globals.clients:
                    i.write_message("pinchange:mcp"+str(self.pin)+":off")
        else:
            gui.change_output_state(self.pin, value)
            GPIO.output(self.pin, int(value))
            if int(value) == 1:
                for i in globals.clients:
                    i.write_message("pinchange:"+str(self.pin)+":on")
            elif int(value) == 0:
                for i in globals.clients:
                    i.write_message("pinchange:"+str(self.pin)+":off")

    def pipe_listener(self):
        while self.keep_piping:
            if self.parent_conn.poll():
                data = self.parent_conn.recv()
                for i in globals.clients:
                    i.write_message(data)
            time.sleep(0.1)
        self.parent_conn.close()

    def start_input_idle(self):
        if self.direction == "in":
            self.idling = True
            self.keep_piping = True
            self.parent_conn, self.child_conn = Pipe()
            self.pipe_thread = Thread(target=self.pipe_listener, args=())
            self.pipe_thread.start()
            self.idle_process = Process(target=self.input_idle, args=(self.child_conn,))
            self.idle_process.start()
        else:
            gui.console("Tried to start idle process on an output!")

    def stop_input_idle(self):
        self.idling = False
        self.keep_piping = False
        time.sleep(0.1)
        if not self.idle_process is None:
            self.idle_process.terminate()
            self.idle_process = None
            self.pipe_thread = None
            self.parent_conn = None
            self.child_conn = None

    def input_idle(self, conn):
        goahead = True
        goahead1 = True
        while True:
            if goahead:
                try:
                    GPIO.wait_for_edge(self.pin, GPIO.RISING)
                    conn.send("inputchange:"+str(self.pin)+":on")
                    gui.change_input_state(self.pin, 1, "reg")
                    goahead1 = True
                except RuntimeError:
                    goahead1 = False
                    time.sleep(0.5)
            if goahead1:
                try:
                    GPIO.wait_for_edge(self.pin, GPIO.FALLING)
                    conn.send("inputchange:"+str(self.pin)+":off")
                    gui.change_input_state(self.pin, 0, "reg")
                    goahead = True
                except RuntimeError:
                    goahead = False
                    time.sleep(0.5)

    def identify(self):
        self.output(1)
        time.sleep(0.5)
        self.output(0)
        time.sleep(0.5)
        self.output(1)
        time.sleep(0.5)
        self.output(0)
        time.sleep(0.5)
        self.output(1)

    def flash(self):
        while True:
            self.output(1)
            time.sleep(0.5)
            self.output(0)
            time.sleep(0.5)

    def toggle(self):
        if self.input() == 0:
            self.output(1)
            return True
        elif self.input() == 1:
            self.output(0)
            return True
        else:
            for i in globals.clients:
                i.write_message("error:Bad toggle on pin "+str(self.pin)+". MCP? "+str(self.mcp)+" State: "+str(self.input()))


class security(object):
    armed_status = False
    watchdog_process = {}
    pipe_threads = {}
    keep_piping = True
    send_disarm = False
    zonedata = None
    tripped = False
    trip_zones = []
    trip_running = False
    alarm_process = {}

    def __init__(self):
        pass

    def arm_system(self, mode):
        globals.cur.execute("SELECT * FROM security_zones")
        self.zonedata = globals.cur.fetchall()
        self.parent_conn, self.child_conn = Pipe()
        self.keep_piping = True
        self.send_disarm = False
        self.mode = mode

        n = 5
        while n != 0:
            gui.console("Security system will be armed in "+str(n)+" seconds")
            n = n - 1
            time.sleep(1)
        for i in self.zonedata:
            if globals.inputs[int(i['pin'])].idling:
                globals.inputs[int(i['pin'])].stop_input_idle()
            else:
                globals.events[globals.inputs[int(i['pin'])].event_id].stop_event()
                globals.inputs[int(i['pin'])].stop_input_idle()
            self.pipe_threads[i['pin']] = Thread(target=self.pipe_listener, args=())
            self.pipe_threads[i['pin']].start()
            self.watchdog_process[i['pin']] = Process(target=self.watchdog, args=(self.child_conn, i['pin'], i['name']))
            self.watchdog_process[i['pin']].start()
        gui.console("System armed!")
        self.armed_status = True

    def disarm_system(self):
        self.tripped = False
        self.keep_piping = False
        self.armed_status = False
        time.sleep(1)
        for i in self.watchdog_process:
            self.watchdog_process[i].terminate()
        self.watchdog_process = {}
        if not self.alarm_process == {}:
            for i in self.alarm_process:
                self.alarm_process[i].terminate()
            self.alarm_process = {}
        for i in self.zonedata:
            if globals.inputs[int(i['pin'])].event_id == None:
                globals.inputs[int(i['pin'])].start_input_idle()
            else:
                globals.events[globals.inputs[int(i['pin'])].event_id].start_event()

    def pipe_listener(self):
        while self.keep_piping:
            if self.parent_conn.poll():
                msg = self.parent_conn.recv()
                data = msg.split(":")
                if data[0] == "zonetrip":
                    self.trip_zones.append(data[1])
                    self.tripped = True
                for i in globals.clients:
                    i.write_message(msg)
            if self.tripped and not self.trip_running:
                thread.start_new_thread(self.alarm_trip, ())
            time.sleep(0.1)
        self.parent_conn.close()

    def alarm_trip(self):
        self.trip_running = True
        globals.cur.execute("SELECT value FROM settings WHERE field = 'alarm timeout'")
        timeout = globals.cur.fetchone()
        n = int(timeout['value'])
        while n != 0:
            gui.console("Zone violation at "+",".join(self.trip_zones)+". Alarm will sound in "+str(n))
            if not self.tripped:
                gui.console("System disarmed. Alarm countdown cancelled")
                self.keep_piping = False
                self.trip_zones = []
                return
            n = n - 1
            time.sleep(1)
        gui.console("Bang")
        for i in globals.outputs:
            self.alarm_process[str(globals.outputs[i].pin)] = Process(target=globals.outputs[i].flash(), args=())
            self.alarm_process[str(globals.outputs[i].pin)].start()

    def watchdog(self, conn, pin, name):
        GPIO.wait_for_edge(int(pin), GPIO.RISING)
        conn.send("zonetrip:"+name)

    def addcamera(self, name, camera_type, camera_address, camera_username, camera_password):
        globals.cur.execute("""INSERT INTO security_cameras VALUES (NULL,%s,NULL,%s,%s,%s,%s)""",(name, camera_type, camera_address, camera_username, camera_password))
        globals.con.commit()
        globals.cur.execute("SELECT id FROM security_cameras WHERE name = '"+name+"'")
        camera_id = globals.cur.fetchone()
        address = 8080 + int(camera_id['id'])
        gui.console(str(address))
        with open("/etc/motion/motion.conf", "a") as motionconf:
            motionconf.write("\nthread /etc/motion/thread"+str(camera_id['id'])+".conf")
        with open("/etc/motion/thread"+str(camera_id['id'])+".conf", "a") as cameraconf:
            if camera_type == "usb":
                cameraconf.write("videodevice /dev/video1\ntext_left "+name+"\ntarget_dir /usr/share/nginx/www/cams/"+name+"\nwebcam_port "+str(address))
        os.makedirs("/usr/share/nginx/www/cams/"+name)
        globals.cur.execute("SELECT value FROM settings WHERE field = 'motion_server'")
        server = globals.cur.fetchone()
        globals.cur.execute("UPDATE security_cameras SET server_address = '"+server['value']+":"+str(address)+"' WHERE id = '"+str(camera_id['id'])+"'")
        globals.con.commit()
        os.system("service motion restart")
        for i in globals.clients:
            i.write_message("refreshpage:")
        gui.gb.screen.refresh()

    def removecamera(self, id):
        globals.cur.execute("DELETE FROM security_cameras WHERE id = '"+str(id)+"'")
        globals.con.commit()
        os.remove("/etc/motion/thread"+str(id)+".conf")
        f = open("/etc/motion/motion.conf","r")
        lines = f.readlines()
        f.close()
        f = open("/etc/motion/motion.conf","w")
        for line in lines:
            if line!="thread /etc/motion/thread"+str(id)+".conf":
                f.write(line)
        f.close()
        os.system("service motion restart")
        gui.gb.screen.refresh()

class sensors(object):
    temp = {}

    def __init__(self):
        #self.temp_process = Process(target=self.record_temp_to_database, args=())
        #self.temp_process.start()
        if globals.nogui:
            self.sensor_gui_refresh = Thread(target=self.refresh_gui_sensors, args=())
            self.run_sensor_refresh = True
            self.sensor_gui_refresh.start()

    def record_temp_to_database(self):
        gui.console("Started temperature recording process")
        globals.cur.execute("SELECT value FROM settings WHERE field = 'temp_interval'")
        interval = globals.cur.fetchone()
        count = 0
        while True:
            if int(count) == int(interval['value']):
                gui.console("Recording current temperatures to database")
                temp = self.temp[globals.sensors_index['temp'][0]]
                globals.cur.execute("""INSERT INTO temperature_records VALUES (NULL,%s,%s,now())""",(globals.temp_sensors[globals.sensors_index['temp'][0]],temp))
                globals.con.commit()
                count = 0
            time.sleep(60)
            count = count + 1

    def refresh_gui_sensors(self):
        gui.console("Started sensor gui refresh process")
        while self.run_sensor_refresh:
            for i in globals.temp_sensors:
                temp = self.get_temperature(sensor_name = i, return_cache = False)
                self.temp[i] = temp
                gui.change_input_state(globals.temp_sensors[i], temp, "temp")
            for i in globals.light_sensors:
                light = self.get_light_level(sensor_name = i)
                gui.change_input_state(globals.light_sensors[i], light, "light")
            time.sleep(5)

    def get_temperature(self, sensor_name = None, return_cache = True):
        if sensor_name != None:
            try:
                sensor_pin = globals.temp_sensors[sensor_name]
            except IndexError:
                return "No sensor"
        else:
            try:
                sensor_pin = globals.temp_sensors[globals.sensors_index['temp'][0]]
            except IndexError:
                return "No sensor"
        if return_cache == True:
            return self.temp[globals.sensors_index['temp'][0]]
        temp = False
        while not temp:
            globals.cur.execute("SELECT type_args FROM inputs WHERE pin = '"+sensor_pin+"'")
            stype = globals.cur.fetchone()
            output = subprocess.check_output(["./utils/env-sensor", stype['type_args'], sensor_pin])
            matches = re.search("Temp =\s+([0-9.]+)", output)
            if (not matches):
                continue
            else:
                temp = float(matches.group(1))
                temp = ((temp * 9) / 5) + 32
                tempdec = str(temp).split('.')
                if float(tempdec[1]) >= 5:
                    tempdec[0] = float(tempdec[0]) + 1
                return str(tempdec[0])

    def get_humidity(self, sensor_name = None):
        if sensor_name != None:
            try:
                sensor_pin = globals.temp_sensors[sensor_name]
            except IndexError:
                return "No sensor"
        else:
            try:
                sensor_pin = globals.temp_sensors[globals.sensors_index['temp'][0]]
            except IndexError:
                return "No sensor"
        humid = False
        while not humid:
            globals.cur.execute("SELECT type_args FROM inputs WHERE pin = '"+sensor_pin+"'")
            stype = globals.cur.fetchone()
            output = subprocess.check_output(["./utils/env-sensor", stype['type_args'], sensor_pin])
            matches = re.search("Hum =\s+([0-9.]+)", output)
            if (not matches):
                continue
            else:
                humid = float(matches.group(1))
                return str(humid)

    def get_light_level(self, sensor_name = None):
        if sensor_name != None:
            try:
                sensor_pin = globals.light_sensors[sensor_name]
            except IndexError:
                return "No sensor"
        else:
            try:
                sensor_pin = globals.light_sensors[globals.sensors_index['light'][0]]
            except IndexError:
                return "No sensor"
        output = subprocess.check_output(["python", "./utils/light.py", sensor_pin])
        output = output.strip(' \t\n\r')
        return output
