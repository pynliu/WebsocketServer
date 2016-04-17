# coding=utf-8
import hashlib,struct
import socket
import threading,random
from base64 import b64encode, b64decode
from xml import parsers
from MyThread import ThreadRun
from socket_data import *

connectionlist = {}
         
def deleteconnection(item):
    global connectionlist
    del connectionlist['connection'+item]
      
class WebSocket(threading.Thread):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    def __init__(self,conn,index,name,remote, path="/"):
        threading.Thread.__init__(self)
        self.conn = conn
        self.index = index
        self.name = name
        self.remote = remote
        self.path = path
        self.buffer = ""     

    def run(self):
        print('Socket%s Start!' % self.index)
        headers = test = {}
        self.handshaken = False
        tr = None
  
        while True:
            if self.handshaken == False:
                print ('Socket%s Start Handshaken with %s!\n' % (self.index,self.remote))
                self.buffer += bytes.decode(self.conn.recv(1024))
 
                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value
  
                    headers["Location"] = ("ws://%s%s" %(headers["Host"], self.path))
                    key = headers['Sec-WebSocket-Key']
                    token = b64encode(hashlib.sha1(str(key + self.GUID)).digest())
 
                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                    "Upgrade: websocket\r\n"\
                    "Connection: Upgrade\r\n"\
                    "Sec-WebSocket-Accept: " + bytes.decode(token) + "\r\n\r\n"
                     
                    self.conn.send(str(handshake))
                    self.handshaken = True  
                    print ('Socket %s Handshaken with %s success!' %(self.index, self.remote))  
                    sendMessage(self.conn,'Welcome, ' + self.name + ' !')  
                else:
                    print ('Socket%s Start Handshaken Fail %s!\n' % (self.index,self.remote))
                    break
                    
            else:
                rev_client = self.conn.recv(128)
                if not rev_client: continue
                client_data = parse_data(rev_client)
                #self.buffer +=client_data
                #print self.buffer
                 
                if 'quit' in client_data:
                    print ('Socket%s Logout!' % (self.index))
                    sendMessage(self.conn,self.name+' Logout')
                    deleteconnection(str(self.index))
                   # self.conn.close()
                    if tr: 
                        tr.stop()
                        tr.join()
                        print "tr closed."
                    self.conn.close()
                    break
                else:
                    print ('%sSocket[%s] msg: %s' % (self.remote, self.index, client_data))
                    # print "[%s] [%s] [%s]" % (self.conn, client_data, tr)
                    tr = ThreadRun(self.conn, client_data, tr)
                    tr.setDaemon(True)
                    tr.start()
            #self.buffer = ""

class WebSocketServer(object):
    def __init__(self):
        self.socket = None
    def begin(self):
        print( 'WebSocketServer Start!')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0",88))
        self.socket.listen(50)
          
        global connectionlist
          
        i=0
        while True:
            connection, address = self.socket.accept()
            #print connection,address
              
            username = address[0]     
            newSocket = WebSocket(connection,i,username,address)
            newSocket.start()
            connectionlist['connection'+str(i)] = connection
            i = i + 1
  
if __name__ == "__main__":
    server = WebSocketServer()
    server.begin()
