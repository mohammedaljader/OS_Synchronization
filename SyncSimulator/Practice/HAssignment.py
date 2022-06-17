from Environment import *

N_CRANE = 5
M_TRUCK = 4

mutex = MyMutex("mutex")
truckSem = MySemaphore(0, "truckSem")
craneSem = MySemaphore(0, "craneSem")


def thread_crane():
    while True:
        mutex.wait()
        print("Loading Container from ship")
        mutex.signal()
        # move to truck platform
        truckSem.wait()
        print("move to truck platform")
        craneSem.signal()

        # move to ship
        print("move to ship()")


def thread_truck():
    while True:
        truckSem.signal()
        print("receive_container_from_crane()")
        craneSem.wait()


def setup():
    for i in range(N_CRANE):
        subscribe_thread(thread_crane)
    for i in range(M_TRUCK):
        subscribe_thread(thread_truck)