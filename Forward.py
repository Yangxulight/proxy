# The Forward class is the one responsible for establishing a connection between the proxy and the remote server(original target).
import socket
import threading
import time
import _thread
from queue import Queue
from Python_proxy import *


# 中继点
class Forward(object):
    """A class for establishing a connection between
        a proxy and a client.
        Since we need to enable two clients to communicante,
        we must esatblish two connections at one time."""
    def __init__(self):
        try:
            #self.client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #self.server_sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            print("Failed to create client socket or server socket.\n")
       #self.client_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
       #self.server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)                    
        
    def connect(self,host_ip,client_port = 8001,server_port=8002):
        #
        #self.server_sock.bind((host_ip,server_port))
        #self.client_sock.listen(1)
        #self.server_sock.listne(1)
        #client_addr_queue = []
        #server_addr_queue = []
        while True:
            #client,c_addr = client_sock.accept()
            #client_addr_queue.append(c_addr)
            #server,s_addr = server_sock.accept()
            client,c_addr = self.socket.accept()
            server,s_addr = self.socket.accept()
            client_thread = threading.Thread(target=to_server,args=(client,s_addr))
            server_thread = threading.Thread(target=to_client,args=(server,c_addr))
            client_thread.start()
            server_thread.start()

    def run(self,host,port):
        print("Running proxy on %s:%s"%(host,str(port)))
        self.socket.bind((host,port))
        self.socket.listen(2)
        while True:
            client,addr = self.socket.accept()
            thread = threading.Thread(target = thread_,args=(self.socket,client,addr))
            thread.start()   

    def close_down(self,server,client):
        server.close()
        client.close()

    def to_server(client,s_addr):
        while True:
            #client.settimeout(5000)
            data_to_server = client.recv(1024)
            client.sendto(data_to_server,s_addr)

    def to_client(server,c_addr):
        while True:
            #server.settimeout(5000) 
            data_to_client = server.recv(1024)
            server.sendto(data_to_client,c_addr)

def thread_(sock,client,addr):
    print("Received data from %s"%str(addr))
    try:
        client.settimeout(5000)
        data_bytes = client.recv(1024)
    except socket.timeout:
        print("timeout error!\n")
    data = data_bytes.decode('utf-8')
    data_split = data.split(' ')
    dist_host = data_split[0]
    dist_port = int(data_split[1])
    msg = data_split[2]
    data = addr[0] + ' ' + str(addr[1]) +' '+ msg
    data_bytes = data.encode('utf-8')
    print("translating data to %s"%dist_host)
    c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect((dist_host,dist_port))
    c.send(data_bytes)
    c.close()
    client.close()
    
    
# thread function get echo message and print
def thread_fun(client,addr):
    print("starting thread\n")
    print("receiving from %s:"% str(client.getpeername())) 
    while True:
        try:
            client.settimeout(500)
            data = client.recv(1024).decode('utf-8')
        except socket.timeout:
            print("time out!\n")
        # if not enter 
        if data != '\r\n' :
            print("%s" % data)
        else:
            break
    print("close client %s...." % str(client.getpeername()))
    client.close()


   
        
    


