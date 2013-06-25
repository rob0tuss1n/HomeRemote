import os
import MySQLdb
import time
import MySQLdb.cursors

try:
    con = MySQLdb.connect('localhost', 'root', 'legoman1', 'automation', cursorclass=MySQLdb.cursors.DictCursor)
except:
    print "Error connecting to mysql!"
    exit()
cur = con.cursor()

while True:
    cur.execute("SELECT * FROM helper_processes")
    proc = cur.fetchall()
    for i in proc:
        print i['pid']
        try:
            os.kill(int(i['pid']), 0)
        except:
            print "Process is dead! Restarting it!"
    time.sleep(3)