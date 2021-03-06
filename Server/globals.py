import sqlite3

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_globals():
    global con
    global cur
    con = sqlite3.connect('/etc/homeremote/database.db')
    con.row_factory = _dict_factory
    cur = con.cursor()
    global blockspi
    global blocki2c
    cur.execute("SELECT value FROM settings WHERE 'settings'.'field'='blockspi'")
    data = cur.fetchone()
    if data['value'] == "y":
        blockspi = True
    cur.execute("SELECT value FROM settings WHERE 'settings'.'field'='blocki2c'")
    data1 = cur.fetchone()
    if data1['value'] == "y":
        blocki2c = True
    global sensors
    global security
    global clients
    clients = []
    global events
    events = {}
    global inputs
    inputs = {}
    global outputs
    outputs = {}
    global nogui
    nogui = False
    global sensors_index
    sensors_index = {"light": [], "temp": []}
    global temp_sensors
    temp_sensors = {}
    global light_sensors
    light_sensors = {}
    global mcp
    mcp = None
    global mcp_loaded
    mcp_loaded = False

