from Environment import *


def threadBaboon(me, other):
    while True:
        mutex.wait()
        me.candidates.v += 1
        if (active_state.v == States.Empty) or (active_state.v == me.activeState):
            active_state.v = me.activeState
            me.sem.signal()
            me.count.v += 1
            me.candidates.v -= 1
        elif active_state.v == other.activeState:
            active_state.v = States.Queued

        mutex.signal()

        me.sem.wait()

        capacity.wait()
        print(f"The thread {me.name} is now in the critical section")
        capacity.signal()

        mutex.wait()
        me.count.v -= 1

        if me.count.v == 0:
            if active_state.v == States.Queued:
                active_state.v = other.activeState
                other.sem.signal(other.candidates.v)
                other.count.v += other.candidates.v
                other.candidates.v -= other.candidates.v
            else:
                active_state.v = States.Empty

        mutex.signal()


class States:
    Empty = "empty"
    South = "South"
    North = "North"
    Queued = "Queued"


class Baboon:
    def __init__(self, count, candidates, sem, activeState, name):
        self.count = count
        self.candidates = candidates
        self.sem = sem
        self.activeState = activeState
        self.name = name


NR_OF_SOUTH_BABOONS = 7
NR_OF_NORTH_BABOONS = 9
active_state = MyString(States.Empty, "state")
mutex = MyMutex("mutex")
capacity = MySemaphore(5, "capacity")

northCount = MyInt(0, "northCount")
northCandidates = MyInt(0, "northCandidates")
northSem = MySemaphore(0, "northSem")

southCount = MyInt(0, "southCount")
southCandidates = MyInt(0, "southCandidates")
southSem = MySemaphore(0, "southSem")

north = Baboon(northCount, northCandidates, northSem, States.North, "North")
south = Baboon(southCount, southCandidates, southSem, States.South, "South")


def setup():
    for i in range(NR_OF_NORTH_BABOONS):
        subscribe_thread(lambda: threadBaboon(north, south))
    for i in range(NR_OF_SOUTH_BABOONS):
        subscribe_thread(lambda: threadBaboon(south, north))