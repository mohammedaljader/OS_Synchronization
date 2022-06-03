from Environment import *

elves = MyInt(0, "elves")
reindeer = MyInt(0, "reindeer")
santaSem = MySemaphore(0, "SantaSemaphore")
reindeerSem = MySemaphore(0, "ReindeerSemaphore")
elvesSem = MySemaphore(0, "elvesSem")
ElfMutex = MyMutex("ElfMutex")
ReindeerMutex = MyMutex("ReindeerMutex")
SantaMutex = MyMutex("SantaMutex")


def santa():
    while True:
        santaSem.wait()
        SantaMutex.wait()
        if elves.v >= 3:
            print("helpElves()")
            elves.v -= 3
            elvesSem.signal()
        elif reindeer.v == 9:
            print("prepareSleigh()")
            reindeer.v -= 9
            reindeerSem.signal()
        SantaMutex.signal()


def elf():
    while True:
        ElfMutex.wait()
        elves.v += 1
        if elves.v >= 3:
            santaSem.signal()
            elvesSem.wait()
            print("getHelp()")
        ElfMutex.signal()


def Reindeer():
    while True:
        ReindeerMutex.wait()
        reindeer.v += 1
        if reindeer.v == 9:
            santaSem.signal()
            reindeerSem.wait()
            print("getHitched()")
        ReindeerMutex.signal()


def setup():
    subscribe_thread(santa)
    subscribe_thread(Reindeer)
    for i in range(7):
        subscribe_thread(elf)

