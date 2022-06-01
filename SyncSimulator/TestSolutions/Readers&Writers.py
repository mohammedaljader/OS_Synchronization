# Readers&Writers
from Environment import *

readers = MyInt(0, "readers")  # How many readers are in the room
mutex = MyMutex(1)  # mutex to protect the readers counter
roomEmpty = MySemaphore(1, "roomEmpty")  # initially it is empty
turnStile = MySemaphore(1, "turnStile")


def Writer():
    while True:
        turnStile.wait()
        roomEmpty.wait()
        print("Only one Writer on the room!!")
        turnStile.signal()
        roomEmpty.signal()


def Reader():
    while True:
        turnStile.wait()
        turnStile.signal()
        mutex.wait()
        readers.v += 1
        if readers.v == 1:
            roomEmpty.wait()
        mutex.signal()

        print(f"{readers.v} readers are now in the room!")

        mutex.wait()
        readers.v -= 1
        if readers.v == 0:
            roomEmpty.signal()
        mutex.signal()


def setup():
    subscribe_thread(Writer)
    subscribe_thread(Reader)
