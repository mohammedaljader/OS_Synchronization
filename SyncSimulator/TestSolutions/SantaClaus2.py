from Environment import *

santaSem = MySemaphore(0, "santaSem")
needHelpBarrier = MySemaphore(0, "needHelpQueue")
helpedBarrier = MySemaphore(0, "helpedQueue")
doneHelping = MySemaphore(0, "doneHelping")
reindeerBarrier = MySemaphore(0, "reindeerQueue")
mutex = MyMutex("mutex")
elfMutex = MyMutex("elfMutex")
reindeer = MyInt(0, "reindeer")
elves = MyInt(0, "elves")
isHelped = MyBool(False, "isHelped")
isThreeElves = MyBool(False, "isThreeElves")
isGetHelp = MyBool(False, "isGetHelp")
isReady = MyBool(False, "isReady")


def santa():
    while True:
        santaSem.wait()
        mutex.wait()
        if elves.v >= 3:
            isThreeElves.v = True
            print("helpElves()")
            needHelpBarrier.signal(elves.v)
            doneHelping.wait()
        elif reindeer.v == 9:
            print("prepareSleigh()")
            reindeerBarrier.signal(9)
            reindeer.v -= 9
            isReady.v = True
        mutex.signal()


def elf():
    while True:
        if not isHelped.v:
            mutex.wait()
            elves.v += 1
            if elves.v == 3:
                santaSem.signal()
                isHelped.v = True
            mutex.signal()
        if isThreeElves.v:
            needHelpBarrier.wait()
            print("getHelp()")
            isGetHelp.v = True
            isHelped.v = True
            isThreeElves.v = False
        if isGetHelp.v:
            elfMutex.wait()
            elves.v -= 1
            if elves.v == 0:
                doneHelping.signal()
                isHelped.v = False
                isGetHelp.v = False
            elfMutex.signal()


def Reindeer():
    while True:
        mutex.wait()
        reindeer.v += 1
        if reindeer.v == 9:
            santaSem.signal()
        mutex.signal()
        if isReady.v:
            reindeerBarrier.wait()
            print("getHitched()")
            isReady.v = False


def setup():
    subscribe_thread(santa)
    subscribe_thread(elf)
    subscribe_thread(Reindeer)
