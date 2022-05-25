from Environment import *

semaphore1 = MySemaphore(0, "semaphore1")
semaphore2 = MySemaphore(0, "semaphore2")
semaphore3 = MySemaphore(0, "semaphore3")
semaphore4 = MySemaphore(0, "semaphore4")


def ThreadA():
    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore1.wait()
    semaphore1.wait()
    semaphore1.wait()
    semaphore1.wait()

    print("Critical Section!")

    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore1.wait()
    semaphore1.wait()
    semaphore1.wait()
    semaphore1.wait()
    print("Out!")


def ThreadB():
    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore2.wait()
    semaphore2.wait()
    semaphore2.wait()
    semaphore2.wait()

    print("Critical Section!")

    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore2.wait()
    semaphore2.wait()
    semaphore2.wait()
    semaphore2.wait()
    print("Out!")


def ThreadC():
    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore3.wait()
    semaphore3.wait()
    semaphore3.wait()
    semaphore3.wait()

    print("Critical Section!")

    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore3.wait()
    semaphore3.wait()
    semaphore3.wait()
    semaphore3.wait()
    print("Out!")


def ThreadD():
    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore4.wait()
    semaphore4.wait()
    semaphore4.wait()
    semaphore4.wait()

    print("Critical Section!")

    semaphore1.signal()
    semaphore2.signal()
    semaphore3.signal()
    semaphore4.signal()

    semaphore4.wait()
    semaphore4.wait()
    semaphore4.wait()
    semaphore4.wait()

    print("Out!")


def setup():
    subscribe_thread(ThreadA)
    subscribe_thread(ThreadB)
    subscribe_thread(ThreadC)
    subscribe_thread(ThreadD)
