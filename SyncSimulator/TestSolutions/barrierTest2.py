from Environment import *

N = 5


class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = MyMutex(1)
        self.turnstile = MySemaphore(0, "turnstile")
        self.turnstile2 = MySemaphore(0, "turnstile2")

    def phase1(self):
        self.mutex.wait()
        self.count += 1
        if self.count == self.n:
            self.turnstile.signal(self.n)
        self.mutex.signal()
        self.turnstile.wait()
        print("Critical")

    def phase2(self):
        self.mutex.wait()
        self.count -= 1
        if self.count == 0:
            self.turnstile2.signal(self.n)
        self.mutex.signal()
        self.turnstile2.wait()

    def wait(self):
        self.phase1()
        self.phase2()


def setup():
    barrier = Barrier(N)
    for i in range(N):
        subscribe_thread(barrier.wait)


