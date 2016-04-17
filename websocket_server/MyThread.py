# -*- coding: utf8 -*-
import sys,os
import time 
import subprocess
import threading
from socket_data import *
 
class ThreadRun(threading.Thread):
    def __init__(self, conn, client_data, tr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_data = client_data
        self.tr = tr
        self.RunScript = os.getcwd() + '/script.sh %s' % self.client_data   ############
        if tr:
            tr.stop()
            tr.join()

    def run(self):
        popen = subprocess.Popen(['bash', '-c', self.RunScript], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.pid = popen.pid
        print('Popen.pid:' + str(self.pid))
        self.ifdo = True;
        while self.ifdo:
            #line = popen.stdout.readline().strip()
            line = popen.stdout.readline()
            sendMessage(self.conn, line)
            if subprocess.Popen.poll(popen) is not None:
                sendMessage(self.conn,'SUCCESS!')
                break
        if os.path.isdir('/proc/%s' % str(self.pid)):
            os.kill(self.pid, 9)
            print "kill %d done" % self.pid

    def stop (self):
        print 'I am stopping it...'
        self.ifdo = False;

