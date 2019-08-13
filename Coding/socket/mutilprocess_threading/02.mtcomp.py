from faker import Factory
import time

faker = Factory.create()
cnt = 10000
x1 = [faker.paragraph() for i in range(cnt)]
x2 = [faker.paragraph() for i in range(cnt)]

print(x1)

start = time.time()

for one in x1:
    len(one)

for one in x2:
    len(one)
end = time.time()

print(end - start)

import threading


class A(threading.Thread):
    def __init__(self, x):
        threading.Thread.__init__(self)
        self.x = x

    def run(self):
        for each in self.x:
            len(each)


t1 = A(x1)
t2 = A(x2)
start1 = time.time()
t1.start()
t2.start()
t1.join()
t2.join()

end1 = time.time()

print(end1 - start1)
print((end1 - start1) / (end - start))
