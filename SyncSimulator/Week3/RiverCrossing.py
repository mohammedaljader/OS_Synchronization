from Environment import *

serfSem = MySemaphore(0, "serfSemaphore")
hackerSem = MySemaphore(0, "hackerSemaphore")
barrier = MyBarrier(4, "barrier")
Multiplex = MySemaphore(5, "multiplex")
passengersMutex = MyMutex("passengersMutex")
mutex = MyMutex("SMutex")
serfs = MyInt(0, "SerfCounter")
hackers = MyInt(0, "HackerCounter")
passengers = MyInt(0, "PassengerCount")


def RiverCrossingThread(me, other, meSem, otherSem, meName):
    while True:
        Multiplex.wait()
        mutex.wait()

        me.v += 1
        if me.v == 4:
            meSem.signal(4)
            me.v = 0
        elif me.v >= 2 and other.v >= 2:
            meSem.signal(2)
            otherSem.signal(2)
            me.v -= 2
            other.v -= 2

        mutex.signal()
        meSem.wait()
        print(f"Board {meName}")

        passengersMutex.wait()
        passengers.v += 1
        if passengers.v == 4:
            print("rowBoat")
            passengers.v = 0
        passengersMutex.signal()

        barrier.wait()
        Multiplex.signal()


def setup():
    for i in range(7):
        subscribe_thread(lambda: RiverCrossingThread(serfs, hackers, serfSem, hackerSem, "Serfs"))
        subscribe_thread(lambda: RiverCrossingThread(hackers, serfs, hackerSem, serfSem, "Hackers"))
