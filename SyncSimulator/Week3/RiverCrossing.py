from Environment import *

serfSem = MySemaphore(0, "serfSemaphore")
hackerSem = MySemaphore(0, "hackerSemaphore")
barrier = MyBarrier(4, "boatBarrier")
Multiplex = MySemaphore(5, "Multiplex")
boatMutex = MyMutex("boatMutex")
SMutex = MyMutex("SMutex")
HMutex = MyMutex("HMutex")
serfs = MyInt(0, "SerfCounter")
hackers = MyInt(0, "HackerCounter")
passengers = MyInt(0, "PassengerCount")


def SerfsThread():
    while True:
        Multiplex.wait()
        SMutex.wait()

        serfs.v += 1
        if serfs.v == 4:
            serfSem.signal(4)
            serfs.v = 0
        elif serfs.v >= 2 and hackers.v >= 2:
            serfSem.signal(2)
            hackerSem.signal(2)
            serfs.v -= 2
            hackers.v -= 2

        SMutex.signal()
        serfSem.wait()
        print("Board Serf")

        boatMutex.wait()
        passengers.v += 1
        if passengers.v == 4:
            print("rowBoat")
            passengers.v = 0
        boatMutex.signal()

        barrier.wait()
        Multiplex.signal()


def HackersThread():
    while True:
        Multiplex.wait()
        HMutex.wait()

        hackers.v += 1
        if hackers.v == 4:
            hackerSem.signal(4)
            hackers.v = 0
        elif hackers.v >= 2 and serfs.v >= 2:
            hackerSem.signal(2)
            serfSem.signal(2)
            hackers.v -= 2
            serfs.v -= 2

        HMutex.signal()
        hackerSem.wait()
        print("Board Hacker")

        boatMutex.wait()
        passengers.v += 1
        if passengers.v == 4:
            print("rowBoat")
            passengers.v = 0
        boatMutex.signal()

        barrier.wait()
        Multiplex.signal()


def setup():
    for i in range(7):
        subscribe_thread(SerfsThread)

    for i in range(7):
        subscribe_thread(HackersThread)
