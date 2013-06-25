import RPi.GPIO as GPIO
import MySQLdb
import MySQLdb.cursors
from multiprocessing import Process, Pipe
import thread
from threading import Thread
import time
import gui

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

global clients
global events
clients = []
events = {}
outputs = {}
inputs = {}

try:
    con = MySQLdb.connect('localhost', 'root', 'legoman1', 'automation', cursorclass=MySQLdb.cursors.DictCursor)
except:
    print "Error connecting to mysql!"
    exit()
cur = con.cursor()

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
    
    def __init__(self, id, cur):
        self.pipe_thread = Thread(target=self.pipe_listen, args=())
        self.cur = cur
        self.id = id
        self.cur.execute("""SELECT * FROM events1 WHERE id = %s""",(self.id))
        data = self.cur.fetchone()
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
                        events[data[1]].start_event()
                    elif data[2] == "off":
                        events[data[1]].stop_event()
                for i in clients:
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
            cur.execute("""DELETE FROM helper_processes WHERE pid = %s""",(self.event_process.pid))
            con.commit()
            self.event_process.terminate()
            self.event_process = None
        gui.change_event_state(self.id, 0)
        self.keep_piping = False
        if self.has_input:
            inputs[self.trigger].start_input_idle()
            
    def run_event(self):
        if self.action == "output_toggle_on_input_timeout":
            self.event_process = Process(target=self.output_toggle_on_input_timeout, args=(self.child_conn,))
            self.has_input = True
            inputs[self.trigger].event_id = self.id
            inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_toggle_on_input":
            self.event_process = Process(target=self.output_toggle_on_input, args=(self.child_conn,))
            self.has_input = True
            inputs[self.trigger].event_id = self.id
            inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_off_on_input":
            self.event_process = Process(target=self.output_off_on_input, args=(self.child_conn,))
            self.has_input = True
            inputs[self.trigger].event_id = self.id
            inputs[self.trigger].stop_input_idle()
            
        elif self.action == "output_on_on_input":
            self.event_process = Process(target=self.output_on_on_input, args=(self.child_conn,))
            self.has_input = True
            inputs[self.trigger].event_id = self.id
            inputs[self.trigger].stop_input_idle()
            
        elif self.action == "event_disable_on_input":
            self.event_process = Process(target=self.event_disable_on_input, args=(self.child_conn,))
            self.has_input = True
            inputs[self.trigger].event_id = self.id
            inputs[self.trigger].stop_input_idle()
            
        elif self.action == "event_enable_on_input":
            self.event_process = Process(target=self.event_enable_on_input, args=(self.child_conn,))
            self.has_input = True
            inputs[self.trigger].event_id = self.id
            inputs[self.trigger].stop_input_idle()
            
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
        cur.execute("""INSERT INTO helper_processes VALUES (%s,%s,%s)""",(self.event_process.pid, "event", self.id))
        con.commit()
        gui.change_event_state(self.id, 1)
        
    def idle_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.BOTH)
            conn.send("inputchange:"+str(self.trigger)+":on")
            gui.change_input_state(str(self.trigger), 1)
            GPIO.wait_for_edge(int(self.trigger), GPIO.BOTH)
            conn.send("inputchange:"+str(self.trigger)+":off")
            gui.change_input_state(self.trigger, 0)
            
    def output_toggle_on_input_timeout(self, conn):
        while True:
            alreadyon = []
            GPIO.wait_for_edge(int(self.trigger), GPIO.BOTH)
            conn.send("inputchange:"+str(self.trigger)+":on")
            gui.change_input_state(int(self.trigger), 1)
            for i in self.who:
                if GPIO.input(int(i)) == 0:
                    alreadyon.append(i)
                    gui.console("Pin already on")
                else:
                    GPIO.output(int(i), 0)
                    gui.change_output_state(int(i), 1)
                    conn.send("pinchange:"+i+":on")
            targettime = int(time.time()) + int(self.timeout)
            changed = False
            while not targettime == int(time.time()):
                if GPIO.input(int(self.trigger)):
                    if changed:
                        conn.send("inputchange:"+str(self.trigger)+":on")
                        gui.change_input_state(int(self.trigger), 1)
                        changed = False
                    targettime = int(time.time()) + self.timeout - 3
                else:
                    changed = True
                    conn.send("inputchange:"+str(self.trigger)+":off")
                    gui.change_input_state(int(self.trigger), 0)
                time.sleep(0.2)
            for i in self.who:
                if not i in alreadyon:
                    GPIO.output(int(i), 1)
                    conn.send("pinchange:"+i+":off")
                    gui.change_output_state(int(i), 0)
                    
    # Toggles all pins to same state first of which was not the previous state in this function
    def output_toggle_on_input(self, conn):
        state = 0
        while True:
            alreadyon = []
            GPIO.wait_for_edge(self.trigger, GPIO.RISING)
            conn.send("inputchange:"+str(self.trigger)+":on")
            gui.change_input_state(self.trigger, 1)
            for i in self.who:
                GPIO.output(int(i), state)
                gui.change_output_state(i, not state)
                if state == 0:
                    state = 1
                else:
                    state = 0
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            gui.change_input_state(self.trigger, 0)
                    
    def output_off_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1)
            for i in self.who:
                GPIO.output(int(i), 1)
                gui.change_output_state(i, 0)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_input_state(self.trigger, 0)
         
    def output_on_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1)
            for i in self.who:
                GPIO.output(int(i), 0)
                gui.change_output_state(i, 1)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_output_state(self.trigger, 0)
            
    def event_enable_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1)
            conn.send("eventchange:"+self.who+":enable")
            gui.change_event_state(self.who, 1)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_event_state(self.trigger, 0)
            
    def event_disable_on_input(self, conn):
        while True:
            GPIO.wait_for_edge(int(self.trigger), GPIO.RISING)
            conn.send("inputchange:"+self.trigger+":on")
            gui.change_input_state(self.trigger, 1)
            conn.send("eventchange:"+self.who+":disable")
            gui.change_event_state(self.who, 0)
            GPIO.wait_for_edge(int(self.trigger), GPIO.FALLING)
            conn.send("inputchange:"+self.trigger+":off")
            gui.change_input_state(self.trigger, 0)
            
    def output_on_at_time(self, conn):
        while True:
            nowtime = time.strftime("%I:%M %p", time.localtime())
            if self.trigger == nowtime:
                for i in self.who:
                    GPIO.output(int(i), 0)
                    gui.change_output_state(i, 1)
            time.sleep(60)
            
    def output_off_at_time(self, conn):
        while True:
            nowtime = time.strftime("%I:%M %p", time.localtime())
            if self.trigger == nowtime:
                for i in self.who:
                    GPIO.output(int(i), 1)
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
    state = None
    name = None
    direction = None
    used = False
    keep_piping = True
    manual_on = False
    event_id = None
    
    def __init__(self, pin, name, direction):
        self.pin = int(pin)
        self.name = name
        self.state = 0
        self.direction = direction
        if direction == "out":
            thread.start_new_thread(self.identify, ())
            pass
        if(direction == "out"):
            GPIO.setup(int(pin), GPIO.OUT)
            gui.add_output(name, pin)
        elif(direction == "in"):
            GPIO.setup(int(pin), GPIO.IN)
            gui.add_input(name, pin)
            self.start_input_idle()
        else:
            gui.console("Failed to setup GPIO!\nUnrecognized direction!")
            return
        gui.console("Setup new GPIO. Pin: " + str(pin) + ", Name: " + name + ", Direction: " + direction)
        
    def set_state(self, state):
        if self.direction == "in":
            return "This is an input!"
        if int(state) == 1:
            if self.state is 1:
                return "Output already set to on"
            else:
                GPIO.output(self.pin, 0)
                gui.change_output_state(self.pin, 1)
                self.state = 1
                return True;
        elif int(state) == '0':
            if self.state is 0:
                return "Output already set to off"
            else:
                GPIO.output(self.pin, 1)
                gui.change_output_state(self.pin, 0)
                self.state = 0
                return True
                
    def get_state(self):
        state = GPIO.input(self.pin)
        if state:
            return False
        else:
            return True
            
    def pipe_listener(self):
        while self.keep_piping:
            if self.parent_conn.poll():
                data = self.parent_conn.recv()
                for i in clients:
                    i.write_message(data)
            time.sleep(0.1)
        self.parent_conn.close()
            
    def start_input_idle(self):
        self.idling = True
        self.keep_piping = True
        self.parent_conn, self.child_conn = Pipe()
        self.pipe_thread = Thread(target=self.pipe_listener, args=())
        self.pipe_thread.start()
        self.idle_process = Process(target=self.input_idle, args=(self.child_conn,))
        self.idle_process.start()
        
    def stop_input_idle(self):
        self.idling = False
        self.keep_piping = False
        time.sleep(0.1)
        self.idle_process.terminate()
        self.idle_process = None
        self.pipe_thread = None
        self.parent_conn = None
        self.child_conn = None
        
    def input_idle(self, conn):
        while True:
            GPIO.wait_for_edge(self.pin, GPIO.RISING)
            conn.send("inputchange:"+str(self.pin)+":on")
            gui.change_input_state(self.pin, 1)
            GPIO.wait_for_edge(self.pin, GPIO.FALLING)
            conn.send("inputchange:"+str(self.pin)+":off")
            gui.change_input_state(self.pin, 0)
        
    def change_direction(self):
        if self.direction == "in":
            GPIO.setup(self.pin, GPIO.OUT)
            print "Pin changed dir"
       
    def waitforinput(self):
        if self.direction == "in":
            GPIO.wait_for_edge(self.pin, GPIO.BOTH)
        else:
            return "This is an output!"
                
    def identify(self):
        GPIO.output(self.pin, 1)
        time.sleep(0.5)
        GPIO.output(self.pin, 0)
        time.sleep(0.5)
        GPIO.output(self.pin, 1)
        time.sleep(0.5)
        GPIO.output(self.pin, 0)
        time.sleep(0.5)
        GPIO.output(self.pin, 1)
        
    def toggle(self, clients):
        if self.get_state() == 1:
            GPIO.output(self.pin, 1)
            gui.change_output_state(self.pin, 0)
            self.state = 0
            self.manual_on = False
            for i in clients:
                i.write_message("pinchange:"+str(self.pin)+":off")
            return True;
        elif self.get_state() == 0:
            GPIO.output(self.pin, 0)
            gui.change_output_state(self.pin, 1)
            self.manual_on = True
            self.state = 1
            for i in clients:
                i.write_message("pinchange:"+str(self.pin)+":on")
            return True;
            
    def wait_for_input_tohigh(self):
        GPIO.wait_for_edge(self.pin, GPIO.RISING)
     
    def wait_for_input_tolow(self):
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)
        

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
    
    def __init__(self):
        pass
        
    def arm_system(self, mode):
        cur.execute("SELECT * FROM security_zones")
        self.zonedata = cur.fetchall()
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
            if inputs[int(i['pin'])].idling:
                inputs[int(i['pin'])].stop_input_idle()
            else:
                events[inputs[int(i['pin'])].event_id].stop_event()
                inputs[int(i['pin'])].stop_input_idle()
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
        for i in self.zonedata:
            if inputs[int(i['pin'])].event_id == None:
                inputs[int(i['pin'])].start_input_idle()
            else:
                events[inputs[int(i['pin'])].event_id].start_event()
            
    def pipe_listener(self):
        while self.keep_piping:
            if self.parent_conn.poll():
                msg = self.parent_conn.recv()
                data = msg.split(":")
                if data[0] == "zonetrip":
                    self.trip_zones.append(data[1])
                    self.tripped = True
                for i in clients:
                    i.write_message(msg)
            if self.tripped and not self.trip_running:
                thread.start_new_thread(self.alarm_trip, ())
            time.sleep(0.1)
        self.parent_conn.close()
        
    def alarm_trip(self):
        self.trip_running = True
        cur.execute("SELECT value FROM settings WHERE field = 'alarm timeout'")
        timeout = cur.fetchone()
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
            
    def watchdog(self, conn, pin, name):
        GPIO.wait_for_edge(int(pin), GPIO.RISING)
        conn.send("zonetrip:"+name)