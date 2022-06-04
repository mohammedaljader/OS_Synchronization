from Environment import *

semaphoreA = MySemaphore(1, "semaphoreA")
semaphoreB = MySemaphore(1, "semaphoreB")
semaphoreC = MySemaphore(1, "semaphoreC")


def threadA():
    while True:
        semaphoreA.wait()

        semaphoreC.wait()

        semaphoreC.signal()

        semaphoreA.signal()


def threadB():
    while True:
        semaphoreB.wait()

        semaphoreA.wait()

        semaphoreA.signal()

        semaphoreB.signal()


def threadC():
    while True:
        semaphoreC.wait()

        semaphoreB.wait()

        semaphoreB.signal()

        semaphoreC.signal()


def setup():
    subscribe_thread(threadA)
    subscribe_thread(threadB)
    subscribe_thread(threadC)