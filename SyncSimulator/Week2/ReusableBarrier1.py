from Environment import *

N = 5

mutex = MyMutex(1)
turnStile1 = MySemaphore(0, "turnStile1")
turnStile2 = MySemaphore(1, "turnStile2")
sem = MySemaphore(0, "semCount")

count = MyInt(0, "count")


def ThreadN():
    mutex.wait()
    sem.signal()
    if sem.get_value() == N:
        turnStile1.signal(N)

    mutex.signal()

    turnStile1.wait()
    turnStile1.signal()

    print("Critical Section!!")

    mutex.wait()
    sem.wait()
    if sem.get_value() == 0:
        turnStile2.signal(N)

    mutex.signal()

    turnStile2.wait()
    turnStile2.signal()
    print("Out from turnstile")


def setup():
    for i in range(N):
        subscribe_thread(ThreadN)
