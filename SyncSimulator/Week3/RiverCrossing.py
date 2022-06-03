# River Crossing
from Environment import *

serfSem = MySemaphore(0, "serfSemaphore")
hackerSem = MySemaphore(0, "hackerSemaphore")
barrier = MyBarrier(4, "barrier")   # Barrier added to make sure that all passengers go at the same time
Multiplex = MySemaphore(5, "multiplex")  # multiplex added to make sure that only one boat can go
passengersMutex = MyMutex("passengersMutex")
mutex = MyMutex("mutex")
serfs = MyInt(0, "SerfCounter")
hackers = MyInt(0, "HackerCounter")
passengers = MyInt(0, "PassengerCount")


def RiverCrossingThread(me, other):
    while True:
        Multiplex.wait()
        mutex.wait()

        me.counter += 1
        if me == 4:
            me.sem.signal(4)
            me.counter = 0
        elif me.counter >= 2 and other.counter >= 2:
            me.sem.signal(2)
            other.sem.signal(2)
            me.counter -= 2
            other.counter -= 2

        mutex.signal()
        me.sem.wait()
        print(f"Board {me.name}")

        passengersMutex.wait()
        passengers.v += 1
        if passengers.v == 4:
            print("rowBoat")
            passengers.v = 0
        passengersMutex.signal()

        barrier.wait()
        Multiplex.signal()


class Person:
    def __init__(self, counter, sem, name):
        self.counter = counter
        self.sem = sem
        self.name = name


serfsClass = Person(serfs.v, serfSem, "serfs")
hackersClass = Person(hackers.v, hackerSem, "hackers")


def setup():
    for i in range(7):
        subscribe_thread(lambda: RiverCrossingThread(serfsClass, hackersClass))
        subscribe_thread(lambda: RiverCrossingThread(hackersClass, serfsClass))
