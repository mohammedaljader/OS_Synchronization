from Environment import *

elves = MyInt(0, "elves")
reindeer = MyInt(0, "reindeer")
santaSem = MySemaphore(0, "santaSem")
reindeerSem = MySemaphore(0, "reindeerSem")
elfTex = MyMutex("elfTex")
mutex = MyMutex("mutex")


def Santa():
    while True:
        santaSem.wait()
        mutex.wait()
        if elves.v == 3:
            print("helpElves")
        elif reindeer.v >= 9:
            print("prepareSleigh")
            reindeerSem.signal(9)
            reindeer.v -= 9

        mutex.signal()


def Reindeer():
    while True:
        mutex.wait()
        reindeer.v += 1
        if reindeer.v == 9:
            santaSem.signal()
        mutex.signal()

        reindeerSem.wait()
        print("getHitched")


def Elves():
    while True:
        elfTex.wait()
        mutex.wait()
        elves.v += 1
        if elves.v == 3:
            santaSem.signal()
        else:
            elfTex.signal()
        mutex.signal()
        print("getHelp")
        mutex.wait()
        elves.v -= 1
        if elves.v == 0:
            elfTex.signal()
        mutex.signal()


def setup():
    subscribe_thread(Santa)
    for i in range(8):
        subscribe_thread(Reindeer)
    for i in range(8):
        subscribe_thread(Elves)
