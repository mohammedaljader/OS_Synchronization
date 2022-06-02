# SantaClaus

# -there are 9 reindeer threads
#
# -there are n elf threads
#
# -santa needs to help _at least_ 3 elves, can be more
#
# -reindeer do **not** have priority
#
# -the elves `getHelp()` must be executed in conjunction with santa's `helpElves()`
#
# -solution must work with **any** number of elves
#
#
# helping the elves: after the third elf arrives, a semaphore must be switched allowing santa to go to the help
# section, when there, santa locks the help section for the elves and calls help with all elves that were able to
# queue in in-time
#
# hitching the reindeer: after all 9 reindeer arrive, they signal santa, who will in turn release their barrier,
# allowing them to enter the critical section. They should then invoke `getHitched()` after santa has invoked
# `prepareSleigh()`
#
# the santa semaphore indicates that either the reindeer or the elves can be helped.
# Santa can only help either the elves or the reindeer in one iteration of the loop
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
        if reindeer.v >= 9:
            print("prepareSleigh")
            reindeerSem.signal(9)
            reindeer.v -= 9
        else:
            print("helpElves")

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
    subscribe_thread(Reindeer)
    subscribe_thread(Elves)
