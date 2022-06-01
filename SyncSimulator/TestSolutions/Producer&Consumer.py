# Producer&Consumer
from Environment import *

bufferSize = 9

mutex = MyMutex(1)
items = MySemaphore(0, "items")
spaces = MySemaphore(bufferSize, "bufferSize")


def Producer():
    while True:
        print("Waiting for event")
        spaces.wait()
        mutex.wait()
        print("add event")
        mutex.signal()
        items.signal()


def Consumer():
    while True:
        items.wait()
        mutex.wait()
        print("get event")
        mutex.signal()
        spaces.signal()
        print("process event")


def setup():
    subscribe_thread(Producer)
    subscribe_thread(Consumer)
