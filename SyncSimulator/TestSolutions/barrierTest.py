from Environment import *

semaphoreA = MySemaphore(0, "semaphoreA")
semaphoreB = MySemaphore(0, "semaphoreB")
semaphoreC = MySemaphore(0, "semaphoreC")


def threadA():
    while True:
        semaphoreA.wait()
        print("A critical point")
        semaphoreB.signal()
        semaphoreA.wait()


def threadB():
    while True:
        semaphoreB.wait()
        print("B critical point")
        semaphoreC.signal()
        semaphoreB.wait()


def threadC():
    while True:
        semaphoreA.signal()
        semaphoreC.wait()
        print("C critical point")
        semaphoreC.wait()


def setup():
    subscribe_thread(threadA)
    subscribe_thread(threadB)
    subscribe_thread(threadC)
