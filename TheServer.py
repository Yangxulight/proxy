import socket,threading,time
from Python_proxy import *


 # telnet 测试 127.0.1.1 4002 端口，不通
class test_ping_Client(object):
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            print("Failed to create client socket or server socket.\n")
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 

    def run(self,host,port): 
        self.s.bind((host,port))
        self.s.listen(2)
        print("Running server on %s."%str((host,port)))
        while True:
            client,addr = self.s.accept()
            #if addr[0] == '127.0.0.1':
            #    msg = addr[0] + " is a illeagle address, connection break."
            #    print(msg)
            #    msg_bytes = msg.encode('utf-8')
            #    client.sendto(msg_bytes,addr)
            #    client.close()
            #    continue
            # 接受数据然后把回复地址放在包里
            print("Conneted to :%s."%str(addr))
            data_bytes = client.recv(1024)
            data = data_bytes.decode('utf-8')
            data_split = data.split(' ')
            dist_host = data_split[0]
            dist_port = int(data_split[1])
            msg = data_split[2]
            print("Received : " + msg)
            send_msg = "I_know_you_are_there."
            data = addr[0] + ' ' + str(addr[1]) + ' ' + send_msg
            data_bytes = data.encode('utf-8')
            print("Sending to response to %s"%str(addr))
            client.sendall(data_bytes)
            client.close()

test = test_ping_Client()
test.run(Server_Host,Server_Port) 