import socket
from Python_proxy import *



class TheClient(object):
    def __init__(self, **kwargs):
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error:
            print("Error when creating the socket")
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
       # self.socket.bind((Client_Host,Client_Port))
       # self.socket.listen(1)
    
    def run_client(self,proxy_host,proxy_port,data):
        print("Running client on %s"% Client_Host)
        print("Connecting to "+str((proxy_host,proxy_port)))
        addr = (proxy_host,proxy_port)
        self.socket.connect(addr)
        self.socket.send(data)
        #self.socket.sendto(data,(proxy_host,proxy_port))
        recv = self.socket.recv(1024)
        recv = recv.decode('utf-8')
        print("Receving: %s"% recv)
    
    def main(self,proxy_host,proxy_port,data,count=5):
        total = count
        while count:
            count-=1
            print("Turn %d:"%(total-count))
            self.run_client(proxy_host,proxy_port,data)

    

client = TheClient()
data = Server_Host+' '+str(Server_Port)+' '+ "I_want_to_connect_to_you."
data_bytes = data.encode('utf-8')
client.main(Host,Port,data_bytes)
