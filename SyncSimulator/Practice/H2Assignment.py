from Environment import *

M_TRUCK = 4

mutex = MyMutex("mutex")
truckSem = MySemaphore(0, "truckSem")
craneASem = MySemaphore(1, "craneASem")
craneBSem = MySemaphore(0, "craneBSem")


def thread_craneA():
    while True:
        craneASem.wait()
        print("load_container_from_ship() craneA")
        # move to open field and drop container

        # move to ship
        craneASem.signal()


def thread_craneB():
    while True:
        mutex.wait()
        print("Loading Container from ship")
        mutex.signal()
        # move to truck platform
        truckSem.wait()
        print("move to truck platform")
        craneBSem.signal()

        # move to ship
        print("move to ship()")


def thread_truck():
    while True:
        truckSem.signal()
        print("receive_container_from_crane()")
        craneBSem.wait()


def setup():
    subscribe_thread(thread_craneA)
    subscribe_thread(thread_craneB)
    for i in range(M_TRUCK):
        subscribe_thread(thread_truck)
