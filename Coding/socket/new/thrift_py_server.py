from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from tutorial_new import Calculator

class CalculatorHandler:
    def __init__(self):
        self.log = {}

    def reg(self, img_url, win1, win2): 
        print(img_url)
        aaa= win1**win2
        print(aaa)
        return {"img_url": img_url, "aaa": str(aaa)}       
        

if __name__ == '__main__':
    handler = CalculatorHandler()
    processor = Calculator.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    # 1.TSimpleServer
    # 2.TNonblockingServer  (×)
    # 3.THsHaServer模式（半同步半异步） (×)
    # 4.TThreadPoolServer模式   (!)
    # 5.TThreadedSelectorServer (!)
    # 6.TThreadedServer  (!)


    print("start server ....")
    server.serve()
    print('done.server is over')







