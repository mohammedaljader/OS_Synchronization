from Environment import *

sem1 = MySemaphore(0, "sem1")
sem2 = MySemaphore(0, "sem2")


def ThreadA():
    print("a1")
    sem1.signal()
    sem2.wait()
    print("a2")


def ThreadB():
    print("b1")
    sem2.signal()
    sem1.wait()
    print("b2")


def setup():
    subscribe_thread(ThreadA)
    subscribe_thread(ThreadB)
