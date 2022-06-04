# Santa Clause
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
            elvesSem.signal(elves.v)
            elves.v = 0
        elif reindeer.v == 9:
            print("prepareSleigh()")
            reindeerSem.signal(9)
            reindeer.v = 0
        SantaMutex.signal()


def elf():
    while True:
        ElfMutex.wait()
        elves.v += 1
        if elves.v == 3:
            santaSem.signal()
        ElfMutex.signal()
        elvesSem.wait()
        print("getHelp()")


def Reindeer():
    while True:
        ReindeerMutex.wait()
        reindeer.v += 1
        if reindeer.v == 9:
            santaSem.signal()
        ReindeerMutex.signal()
        reindeerSem.wait()
        print("getHitched()")


def setup():
    subscribe_thread(santa)
    for i in range(7):
        subscribe_thread(elf)
    for i in range(9):
        subscribe_thread(Reindeer)
