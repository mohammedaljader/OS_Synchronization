from Environment import *

N = 5

mutex = MyMutex(1)
turnStile1 = MySemaphore(0, "turnStile1")
turnStile2 = MySemaphore(1, "turnStile2")

count = MyInt(0, "count")


def ThreadN():
    mutex.wait()

    count.v += 1
    if count.v == N:
        turnStile2.wait()  # lock the second
        turnStile1.signal()  # unlock the first

    mutex.signal()

    turnStile1.wait()           # first turnstile
    turnStile1.signal()

    print("Critical Section!!")

    mutex.wait()

    count.v -= 1
    if count.v == 0:
        turnStile1.wait()          # lock the first
        turnStile2.signal()        # unlock the second

    mutex.signal()

    turnStile2.wait()             # second turnstile
    turnStile2.signal()


def setup():
    for i in range(N):
        subscribe_thread(ThreadN)
