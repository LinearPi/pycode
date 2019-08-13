from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from tutorial import Calculator
from tutorial.ttypes import Operation, InvalidOperation

import threading


a = []
b = {}
c = []
d = {}
class CalculatorHandler:
    def __init__(self):
        self.log = {}

    def registe(self, img_url):  
        global a
        global b
        global c
        global d
        print(img_url)
        c.append(img_url)
        print(c)
        a.append(1)
        print(a)      
        while True:
            if b != {}:
                d = b
                b = {}
                break
            else:
                pass
        print(b)
        print(0)
        print(d)
        return d      
        
        
           
def detect_img():
    global a
    global b
    global c
    global d
    while True:
        if len(a)==1: 
            try:
                print(c[0])
                image = Image.open(c[0])
                b['a'] = "ok ss"
                a = []               

            except:
                print('Open Error! Try again!')
                continue 
        else:               
            pass
    # yolo.close_session()       



if __name__ == '__main__':
    handler = CalculatorHandler()
    processor = Calculator.Processor(handler)
    transport = TSocket.TServerSocket(host='localhost', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    thread1 = threading.Thread(target=detect_img,name="线程1")

    #创建线程完毕之后，一定要启动
    thread1.start()
    server.serve()
    print('done.')







