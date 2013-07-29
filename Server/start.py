import os
import sys
if __name__ == "__main__":
    try:
        with open('lock.pid'): pass
        print 'Lock file already exists! This probably means HomeRemote is already running or that it was improperly shutdown (crash)\n Delete the lockfile at /etc/remotehome/lock.pid and try again!'
        sys.exit()
    except IOError:
        with open('lock.pid', 'w') as lockfile:
            os.chmod("./lock.pid", 0666)
            lockfile.write(str(os.getpid()))
            lockfile.close()
import RPi.GPIO as GPIO
import globals
import websocketserver
import signal
import gui
from remotehome import gpio, event, security, sensors

def signal_handler(signal, frame):
        # Run all clean-up functions to indicate a safe shutdown
        gui.console('Closing server')
        for i in globals.clients:
            i.close()
        for i in globals.events:
            globals.events[i].stop_event()
        for i in globals.inputs:
            if globals.inputs[i].idling:
                globals.inputs[i].stop_input_idle()
        try:
            sensors.temp_process.terminate()
        except AttributeError:
            pass
        gui.console('Closed vars')
        sensors.run_sensor_refresh = False
        GPIO.cleanup()
        if not globals.nogui:
            gui.end()
        os.remove('lock.pid')
        sys.exit(0)

if __name__ == "__main__":
    globals.init_globals()
    security = security()
    sensors = sensors()

    daemonize = False
    for i in sys.argv:
        if i == "-nogui":
            globals.nogui = True
        if i == "-D":
            daemonize = True
            globals.nogui = True

    if not globals.nogui:
        gui.start()
    if daemonize:
        gui.no_output = True

    # Check for a user on the database. If there isnt one, create a default admin account
    globals.cur.execute("SELECT username FROM accounts")
    accounts = globals.cur.fetchall()
    if not accounts:
        globals.cur.execute("INSERT INTO `main`.`accounts` (`name`, `username`, `password`) VALUES ('admin', 'admin', '7c6a180b36896a0a8c02787eeafb0e4c')")
        globals.con.commit()

    # Get pins and set them up
    globals.cur.execute("SELECT name, pin FROM outputs")
    data = globals.cur.fetchall()
    for i in data:
        globals.outputs[str(i['pin'])] = gpio(i['pin'], i['name'], "none", 'out')

    # Get inputs and set them up
    globals.cur.execute("SELECT name, pin, type FROM inputs")
    data = globals.cur.fetchall()
    for i in data:
        globals.inputs[int(i['pin'])] = gpio(i['pin'], i['name'], i['type'], 'in')

    # Get events and set them up
    globals.cur.execute("SELECT id FROM events")
    eventsdata = globals.cur.fetchall()
    for i in eventsdata:
        globals.events[int(i['id'])] = event(int(i['id']))

    signal.signal(signal.SIGINT, signal_handler)
    websocketserver.start_websocket_server()