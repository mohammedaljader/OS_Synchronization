from Environment import *

N = 7

elves = MyInt(0, "elves")
reindeer = MyInt(0, "reindeer")

santaSem = MySemaphore(0, "SantaSemaphore")
reindeerSem = MySemaphore(0, "ReindeerSemaphore")
elvesSem = MySemaphore(0, "elvesSem")

mutex = MySemaphore(1, "mutex")


def santa():
    while True:
        santaSem.wait()
        if elves.v >= 3:
            print("helpElves()")
            elvesSem.signal()
        elif reindeer.v == 9:
            print("prepareSleigh()")
            reindeerSem.signal()


def elf():
    while True:
        mutex.wait()
        elves.v += 1
        if elves.v >= 3:
            santaSem.signal()
            elvesSem.wait()
            print("getHelp()")
            elves.v -= 3
        mutex.signal()


def reindeer():
    while True:
        if reindeer.v == 9:
            santaSem.signal()
            reindeerSem.wait()
            print("getHitched()")
            reindeer.v = 0
        mutex.wait()
        if reindeer.v < 9:
            reindeer.v += 1
        mutex.signal()


def setup():
    subscribe_thread(santa)
    for i in range(N):
        subscribe_thread(elf)
    for i in range(N):
        subscribe_thread(reindeer)
