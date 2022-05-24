from Environment import *

N = 5

mutex = MyMutex(1)
barrier = MySemaphore(0, "barrier")

count = MyInt(0, "count")


def ThreadN():
    mutex.wait()
    count.v += 1
    mutex.signal()

    if count.v == N:
        barrier.signal()

    barrier.wait()
    barrier.signal()

    print("Critical point!")


def setup():
    for i in range(N):
        subscribe_thread(ThreadN)
