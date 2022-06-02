from Environment import *

santaSem = MySemaphore(0, "santaSem")
needHelpBarrier = MySemaphore(0, "needHelpBarrier")
helpedBarrier = MySemaphore(0, "helpedBarrier")
doneHelping = MySemaphore(0, "doneHelping")
reindeerBarrier = MySemaphore(0, "reindeerBarrier")
elfTurnstile = MySemaphore(1, "elfTurnstile")
mutex = MyMutex("mutex")
elfMutex = MyMutex("elfMutex")
reindeer = MyInt(0, "reindeer")
elves = MyInt(0, "elves")


def santa():
    while True:
        santaSem.wait()
        mutex.wait()
        if elves.v >= 3:
            needHelpBarrier.signal(elves.v)
            print("helpElves()")
            doneHelping.wait()
            helpedBarrier.signal(elves.v)
        elif reindeer.v == 9:
            print("prepareSleigh()")
            reindeerBarrier.signal(9)
            reindeer.v -= 9
            elfTurnstile.signal()
        mutex.signal()


def elf():
    while True:
        elfTurnstile.wait()
        elfTurnstile.signal()
        mutex.wait()
        elves.v += 1
        if elves.v == 3:
            santaSem.signal()
        mutex.signal()
        needHelpBarrier.wait()
        print("getHelp()")
        elfMutex.wait()
        elves.v -= 1
        if elves.v == 0:
            doneHelping.signal()
        elfMutex.signal()
        helpedBarrier.wait()


def Reindeer():
    while True:
        mutex.wait()
        reindeer.v += 1
        if reindeer.v == 9:
            elfTurnstile.wait()
            santaSem.signal()
        mutex.signal()
        reindeerBarrier.wait()
        print("getHitched()")


def setup():
    subscribe_thread(santa)
    subscribe_thread(elf)
    subscribe_thread(Reindeer)
