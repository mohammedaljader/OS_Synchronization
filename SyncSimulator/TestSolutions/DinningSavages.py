# DinningSavages
from Environment import *

servings = MyInt(0, "servings")
mutex = MyMutex("mutex")
emptyPot = MySemaphore(0, "emptyPot")
fullPot = MySemaphore(0, "fullPot")


def cookThread():
    while True:
        emptyPot.wait()
        print("putServingsInPot(M)")
        fullPot.signal()


def savageThread():
    while True:
        mutex.wait()
        if servings.v == 0:
            emptyPot.signal()
            fullPot.wait()
            servings.v = 10
            servings.v -= 1
            print("getServingFromPot ()")
        mutex.signal()
        print("eat()")


def setup():
    subscribe_thread(cookThread)
    subscribe_thread(savageThread)
