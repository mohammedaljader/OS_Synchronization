from Environment import *

N = 5
mutex = MyMutex("mutex")
count = MyInt(0, "Count")
turnstile = MySemaphore(0, "turnstile")


def barrier():
    while True:
        mutex.wait()
        count.v += 1
        mutex.signal()

        if count.v == N:
            turnstile.signal()

        turnstile.wait()
        turnstile.signal()

        print("CS")

        mutex.wait()
        count.v -= 1
        mutex.signal()

        if count.v == 0:
            turnstile.wait()


def setup():
    for i in range(N):
        subscribe_thread(barrier)
