import os
import MySQLdb
import time
import MySQLdb.cursors
import psutil
import logging
logging.basicConfig(filename='/etc/homeremote/helper.log',level=logging.ERROR)

try:
    con = MySQLdb.connect('localhost', 'root', 'legoman1', 'automation', cursorclass=MySQLdb.cursors.DictCursor)
except:
    print "Error connecting to mysql!"
    exit()
cur = con.cursor()

def proc_problem(info):
    logging.error("PID: "+str(info['pid'])+" - Process unexpectedly quit! Checking server lock file!")
    try:
        with open('lock.pid'): pass
        logging.error("PID: "+str(info['pid'])+" - Lock file still exists! There must have been a crash! We will try to restart the process now")
    except IOError:
        logging.error("PID: "+str(info['pid'])+" - Lock file does not exist. Assuming the server made a graceful shutdown")

while True:
    con.commit()
    cur.execute("SELECT * FROM helper_processes")
    proc = cur.fetchall()
    for i in proc:
        try:
            p = psutil.Process(int(i['pid']))
            if str(p.status) == "zombie":
                proc_problem(i)
        except NoSuchProcess:
            proc_problem(i)
    time.sleep(3)