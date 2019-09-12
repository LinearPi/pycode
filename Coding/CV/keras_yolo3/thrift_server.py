from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from tutorial import Calculator
from tutorial.ttypes import Operation, InvalidOperation


class CalculatorHandler:
    def __init__(self):
        self.log = {}

    def registe(self, img_url):        
        print(img_url)
        return {"name":img_url, "address":"在哪里"}

if __name__ == '__main__':
    handler = CalculatorHandler()
    processor = Calculator.Processor(handler)
    transport = TSocket.TServerSocket(host='192.168.1.67', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
    TServer.TServerSocket()