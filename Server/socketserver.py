from socket import *
import thread
import gui
import globals
import serverhandler
 
BUFF = 1024
HOST = '0.0.0.0'# must be input parameter @TODO
PORT = 9001 # must be input parameter @TODO
 
def handler(clientsock,addr):
    globals.clients.append(clientsock)
    while 1:
        data = clientsock.recv(BUFF)
        h = serverhandler.handle(data, Server_type="socket", Conn=clientsock)
        h.handle_client()
    globals.clients.remove(clientsock)
 
def start_sockets():
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    gui.console("Started socket server on port ", str(PORT))
    while 1:
        clientsock, addr = serversock.accept()
        gui.console('...connected from:', addr)
        thread.start_new_thread(handler, (clientsock, addr))