from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket

from tutorial_new import Calculator

import multiprocessing
from multiprocessing import Pool
import time
t1 = time.time()

# Make socket
transport = TSocket.TSocket('127.0.0.1', 9090)

# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)

# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)

# Create a client to use the protocol encoder
client = Calculator.Client(protocol)

# Connect!
transport.open()

cores = multiprocessing.cpu_count()
print(cores)
pool = multiprocessing.Pool(processes=cores)

img_url = "wo shi ni de shei"

sss = client.reg(img_url, 2, 5)

# list_a = [img_url, img_url, img_url, img_url]
# list_b = list(range(4,8))
# print(list_b)
# list_c = range(1,5)

# y = pool.map(client.reg, [list_a, list_b, list_c])
# print(y)


print(time.time() - t1)
print(sss)
