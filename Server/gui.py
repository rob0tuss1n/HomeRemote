import curses
import time
import sys


class gb(object):
    output_objs = {}
    input_objs = {}
    event_objs = {}
    outputs_win = None
    inputs_win = None
    events_win = None
    console_win_sub = None
    console_win_sub_size = None
    obj_line_length = None
    nocolor = False
    
def start(): 
    gb.screen = curses.initscr()
    gb.screen_size = gb.screen.getmaxyx()
    if gb.screen_size[0] < 24 or gb.screen_size[1] < 80:
        end()
        print "\nThe terminal window is too small to use the GUI. Please start without GUI or resize your terminal\n\n"
        print "Current size: " + str(gb.screen_size[1]) + "x" + str(gb.screen_size[0])
        print "Minimum size: 80x24\n"
        sys.exit()
    
    curses.start_color()
    try:
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    except:
        gb.nocolor = True
    try:
        curses.curs_set(0)
    except:
        pass
    
    gb.outputs_win = gb.screen.subwin(gb.screen_size[0] / 4 * 3 - 3, gb.screen_size[1] / 3, 0, 0)
    gb.outputs_win.border(0)
    gb.outputs_win.addstr(0, gb.screen_size[1] / 3 / 2 - 4, " Outputs ")
    
    gb.inputs_win = gb.screen.subwin(gb.screen_size[0] / 4 * 3 - 3, gb.screen_size[1] / 3, 0, gb.screen_size[1] / 3)
    gb.inputs_win.border(0)
    gb.inputs_win.addstr(0, gb.screen_size[1] / 3 / 2 - 4, " Inputs ")
    
    gb.events_win = gb.screen.subwin(gb.screen_size[0] / 4 * 3 - 3, gb.screen_size[1] / 3, 0, gb.screen_size[1] / 3 * 2)
    gb.events_win.border(0)
    gb.events_win.addstr(0, gb.screen_size[1] / 3 / 2 - 3, " Events ")
        
    gb.console_win = gb.screen.subwin(gb.screen_size[0] / 4 + 3, gb.screen_size[1] / 3 * 3, gb.screen_size[0] / 4 * 3 - 3, 0)        
    gb.console_win.border(0)
    gb.console_win.addstr(0, 4, " Console ")
    gb.screen.refresh()
    
    gb.console_win_sub = gb.screen.subwin(gb.screen_size[0] / 4 + 3 - 2, gb.screen_size[1] / 3 * 3 - 4, gb.screen_size[0] / 4 * 3 - 2, 1)
    gb.console_win_sub.scrollok(True)
    gb.console_win_sub_size = gb.console_win_sub.getmaxyx()
    gb.console_win_sub.setscrreg(0, gb.console_win_sub_size[0] - 2)
    
    outputlines = gb.outputs_win.getmaxyx()
    gb.obj_line_length = outputlines[1] - 2
    i = 1;
    while not i == outputlines[0] - 2:
        gb.output_objs[i] = "%empty"
        gb.input_objs[i] = "%empty"
        gb.event_objs[i] = "%empty"
        i = i + 1
                
def console(string):
    gb.console_win_sub.scroll(1)
    gb.console_win_sub.addstr(gb.console_win_sub_size[0] - 2, 0, str(string))
    gb.console_win_sub.refresh()
    
def add_output(name, pin):
    for i in gb.output_objs:
        if gb.output_objs[i] == "%empty":
            gb.outputs_win.addstr(i, 1, name)
            if gb.nocolor:
                gb.outputs_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
            else:
                gb.outputs_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(1))
            gb.outputs_win.refresh()
            gb.output_objs[i] = int(pin)
            break
                
def remove_output(pin):
    for i in gb.output_objs:
        if gb.output_objs[i] == int(pin):
            gb.output_objs[i] = "%empty"
            gb.outputs_win.addstr(i, 1, " "*gb.obj_line_length)
            gb.outputs_win.refresh()
            break
                
def change_output_state(pin, state):
    for i in gb.output_objs:
        if gb.output_objs[i] == int(pin):
            if state == 0:
                if gb.nocolor:
                    gb.outputs_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
                else:
                    gb.outputs_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(1))
            elif state == 1:
                if gb.nocolor:
                    gb.outputs_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
                else:
                    gb.outputs_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(2))
            gb.outputs_win.refresh()
            break
            
def add_input(name, pin):
    for i in gb.input_objs:
        if gb.input_objs[i] == "%empty":
            gb.inputs_win.addstr(i, 1, name)
            gb.inputs_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(1))
            gb.inputs_win.refresh()
            gb.input_objs[i] = int(pin)
            break
        
def remove_input(pin):
    for i in gb.input_objs:
        if gb.input_objs[i] == int(pin):
            gb.input_objs[i] = "%empty"
            gb.inputs_win.addstr(i, 1, " "*gb.obj_line_length)
            gb.inputs_win.refresh()
            break
        
def change_input_state(pin, state):
    for i in gb.input_objs:
        if gb.input_objs[i] == int(pin):
            if state == 0:
                if gb.nocolor:
                    gb.inputs_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
                else:
                    gb.inputs_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(1))
            elif state == 1:
                if gb.nocolor:
                    gb.inputs_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
                else:
                    gb.inputs_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(2))
            gb.inputs_win.refresh()
            break
        
def add_event(name, id):
    for i in gb.event_objs:
        if gb.event_objs[i] == "%empty":
            gb.events_win.addstr(i, 1, name)
            gb.events_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(1))
            gb.events_win.refresh()
            gb.event_objs[i] = int(id)
            break
        
def remove_event(id):
    for i in gb.event_objs:
        if gb.event_objs[i] == int(id):
            gb.event_objs[i] = "%empty"
            gb.events_win.addstr(i, 1, " "*gb.obj_line_length)
            gb.events_win.refresh()
            break
        
def change_event_state(id, state):
    for i in gb.event_objs:
        if gb.event_objs[i] == int(id):
            if state == 0:
                if gb.nocolor:
                    gb.events_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
                else:
                    gb.events_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(1))
            elif state == 1:
                if gb.nocolor:
                    gb.events_win.chgat(i, gb.obj_line_length, 1, curses.A_REVERSE)
                else:
                    gb.events_win.addstr(i, gb.obj_line_length, " ", curses.color_pair(2))
            gb.events_win.refresh()
            break
            
def end():
    curses.endwin()