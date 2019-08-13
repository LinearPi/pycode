from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket
from multiprocessing import Pool

from tutorial import Calculator
import argparse
import time
t1 = time.time()

# Make socket
transport = TSocket.TSocket('localhost', 9090)

# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)

# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)

# Create a client to use the protocol encoder
client = Calculator.Client(protocol)

# Connect!
transport.open()
img_url = r"F:\PYcode\coding\CV\keras_yolo3\data\123.jpg"
# p = Process(target=client.registe, args=(img_url,))
# p.start()
# p.join()

sss = client.registe(img_url)
print(time.time() - t1)
print('do')
print(sss)
