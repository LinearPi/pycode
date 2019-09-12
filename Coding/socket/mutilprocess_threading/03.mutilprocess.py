import multiprocessing
import time

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
            print("this is %s" % self._n)
            time.sleep(1)


if __name__ == "__main__":
    # 使用列表生成式创建4个类
    mt = [A(i) for i in range(10)]
    for i in mt:
        i.start()
    for i in mt:
        i.join()
