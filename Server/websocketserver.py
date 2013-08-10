import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.template
import gui
import thread
import globals
import serverhandler

class WebSocket(tornado.websocket.WebSocketHandler):
    # Handle a new web client
    def open(self):
        globals.clients.append(self)
        gui.console("Websocket Opened")

    def on_message(self, message):
        gui.console(message)
        h = serverhandler.handle(message, Server_type="web", Conn=self)
        h.handle_client()
                
    def on_close(self):
        gui.console("Websocket closed")
        globals.clients.remove(self)

def start_websocket_server():
    application = tornado.web.Application([(r"/", WebSocket),])
    application.listen(9000, '0.0.0.0')
    gui.console("Server started. Waiting for clients")
    tornado.ioloop.IOLoop.instance().start()
