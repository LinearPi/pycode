from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket
from multiprocessing import Pool
import multiprocessing

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


 # 多线程
class A(multiprocessing.Process):
    # 使用threading.Thread 类创建好
    def __init__(self, n):
        # 使用父类进行初始化
        multiprocessing.Process.__init__(self)
        self._n = n

    # 定义一个run方法， thread的主方法
    def run(self):
        while True:
            sss = client.registe(img_url)
            print(sss)
            print("this is %s" % self._n)
            time.sleep(1)


if __name__ == "__main__":
    # 使用列表生成式创建4个类
    mt = [A(i) for i in range(10)]
    for i in mt:
        i.start()
    for i in mt:
        i.join()


    print(time.time() - t1)
    print('do')

