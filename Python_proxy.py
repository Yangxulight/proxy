import socket
import threading
import time
import _thread
import time
from Forward import *
Server_Host = "127.0.1.2"
Client_Host = "127.0.1.1"
Host = "127.0.1.0"
Port = 11111
Client_Port = 22222
Server_Port = 33333
#if __name__ == '__main__':
#    host = '127.0.0.1'
#    port = 4040
#    try:
#        s = socket(AF_INET,SOCK_STREAM)
#    except socket.error:
#        print("Failed to create socket.")
#    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#    s.bind((host,port))
#    s.listen(50)
#    print("Listening on %s:%s"%(host,str(port)))
#    while True:
#        client,addr = s.accept()
#        thread = threading.Thread(target=thread_fun,args=(client,addr))
#        thread.start()
#    s.close()
class TheProxy(object):
    def __init__(self):
        try:
            self.client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)     # connect to server
            self.server_sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)      # receive from client
        except socket.error:
            print("Failed to create client socket or server socket.\n")
       #self.client_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    def run(self,host,port,max_connect=2):
        client_event = threading.Event()
        server_event = threading.Event()
        print("Running server on %s:%d"%(host,port))
        msg_to_client_queue = Queue()
        msg_to_server_queue = Queue()
        self.server_sock.bind((host,port))
        self.server_sock.listen(max_connect)
        receive_from_client_thread = threading.Thread(target=self.receive_from_client,args=(client_event,server_event,self.server_sock,msg_to_client_queue,msg_to_server_queue))
        send_to_server_thread =  threading.Thread(target=self.send_to_server,args=(client_event,server_event,self.client_sock,msg_to_client_queue,msg_to_server_queue))
        receive_from_client_thread.start()
        send_to_server_thread.start() 
        receive_from_client_thread.join()
        send_to_server_thread.join() 

    def send_to_server(self,client_event,server_event,client,msg_2_client,msg_2_server):
        flag=True
        while True:
            server_event.wait() 
            if msg_2_server.empty():
                continue
            else:
                data_bytes = msg_2_server.get()
                dist_addr,msg = self.prase_data(data_bytes)
                print("Translating %s to %s." % (msg,str(dist_addr)))
                response = self.get_response(dist_addr,msg)
                client.connect(dist_addr)
                client.send(data_bytes)
                flag=True
            if msg_2_client.empty() and flag:
                data_to_client = client.recv(1024)
                msg_2_client.put(data_to_client)
                flag=False
                client_event.set()            
            time.sleep(1)

    def receive_from_client(self,client_event,server_event,server,msg_2_client,msg_2_server):
        client,addr = server.accept()
        flag = True
        #client.setblocking(0)
        while True:
            if msg_2_server.empty() and flag:
                data_bytes = client.recv(1024)
                dist_addr,msg = self.prase_data(data_bytes)
                print("Received '%s' from %s."%(msg,str(addr)))
                msg_2_server.put(data_bytes)
                server_event.set()
                flag=False
            if msg_2_client.empty():
               continue
            else:
               data = msg_2_client.get()
               client.sendall(data)
               flag=True
               time.sleep(2)
            client_event.wait()

    def prase_data(self,data_bytes):
        data = data_bytes.decode('utf-8')
        data_split = data.split(' ')
        dist_host = data_split[0]
        dist_port = int(data_split[1])
        addr = ((dist_host,dist_port))
        msg = data_split[2]
        return addr,msg

    # 根据地址，消息，包装响应数据
    def get_response(self,addr,msg):
        data = addr[0] + ' ' + str(addr[1]) +' '+ msg
        data_bytes = data.encode('utf-8')
        return data_bytes


if __name__ == '__main__':
    proxy = TheProxy()
    proxy.run(Host,Port) 