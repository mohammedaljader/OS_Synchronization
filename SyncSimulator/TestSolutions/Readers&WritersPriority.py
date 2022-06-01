# Readers&WritersPriority
from Environment import *

noReaders = MySemaphore(1, "NoReaders")
noWriters = MySemaphore(1, "NoWriters")
readSwitch = MyLightswitch(noWriters)
writerSwitch = MyLightswitch(noReaders)


def Writer():
    while True:
        writerSwitch.lock(noReaders)
        noWriters.wait()
        print("Only one Writer on the room!!")
        noWriters.signal()
        writerSwitch.unlock(noWriters)


def Reader():
    while True:
        noReaders.wait()
        readSwitch.lock(noWriters)
        noReaders.signal()
        print(f"readers are now in the room!")
        readSwitch.unlock(noWriters)


def setup():
    subscribe_thread(Writer)
    subscribe_thread(Reader)
