# from threading import Thread, current_thread, Lock
  
# def add_1():
#     global num
#     lock.acquire()
#     for temp in range(1000000):
#         num += 1
#     lock.release()
#     print("%s的计算结果是:%s" % (current_thread().name, num))
 
 
# def main():
#     t_1 = Thread(target=add_1)
#     t_2 = Thread(target=add_1)
#     t_1.start()
#     t_2.start()
#     t_1.join()
#     t_2.join()
#     print("num的最终结果是:%s" % num)
 
 
# if __name__ == '__main__':
#     lock = Lock()
#     num = 0
#     main()

from threading import Thread, current_thread
 
 
def add_1():
    global num
    for temp in range(1000000):
        num += 1
    print("%s的计算结果是:%s" % (current_thread().name, num))
 
 
def main():
    t_1 = Thread(target=add_1)
    t_2 = Thread(target=add_1)
    t_1.start()
    t_2.start()
    t_1.join()
    t_2.join()
    print("num的最终结果是:%s" % num)
 
 
if __name__ == '__main__':
    num = 0
    main()

