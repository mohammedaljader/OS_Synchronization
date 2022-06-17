from Environment import *


def person_thread(me, other):
    while True:
        mutex.wait()

        me.queueCounter.v += 1

        while state.v == other.transition:
            me.queue_cv.wait()

        me.queueCounter.v -= 1

        me.counter.v += 1

        if state.v == States.NEUTRAL:
            state.v = me.rule

        elif state.v == other.rule and me.counter.v > other.counter.v:
            state.v = me.transition

        while state.v == other.rule or state.v == me.transition:
            me.cv.wait()

        mutex.signal()

        print(f"walking field...{me.name}")

        mutex.wait()

        me.counter.v -= 1

        if state.v == me.rule and other.counter.v > me.counter.v:
            state.v = other.transition

        if state.v == other.transition and me.counter.v == 0:
            state.v = other.rule
            if other.counter.v > 0:
                other.cv.notify_all()
            if me.queueCounter.v > 0:
                me.queue_cv.notify_all()

        if state.v == me.rule and me.counter.v == 0:
            state.v = States.NEUTRAL

        mutex.signal()


class States:
    NEUTRAL = "neutral"
    HEATHENS_RULE = "heathens rule"
    PRUDES_RULE = "prudes rule"
    HEATHENS_TRANSITION = "transitioning to heathens"
    PRUDES_TRANSITION = "transitioning to prudes"


class Person(object):
    def __init__(self, queueCounter, counter, queue_cv, cv, rule, transition, name):
        self.queueCounter = queueCounter
        self.counter = counter
        self.queue_cv = queue_cv
        self.cv = cv
        self.rule = rule
        self.transition = transition
        self.name = name


NR_OF_PRUDES = 6
NR_OF_HEATHENS = 9
mutex = MyMutex("mutex")

heathensQueue_cv = MyConditionVariable(mutex, "heathensQueue_cv")
heathens_cv = MyConditionVariable(mutex, "heathens_cv")

prudesQueue_cv = MyConditionVariable(mutex, "prudesQueue_cv")
prudes_cv = MyConditionVariable(mutex, "prudes_cv")

heathensQueue = MyInt(0, "heathensQueue")
prudesQueue = MyInt(0, "prudesQueue")

heathensCounter = MyInt(0, "heathensCounter")
prudesCounter = MyInt(0, "prudesCounter")

state = MyString(States.NEUTRAL, "state")


def setup():
    prude = Person(prudesQueue, prudesCounter, prudesQueue_cv, prudes_cv, States.PRUDES_RULE,
                   States.PRUDES_TRANSITION, "prude")
    heathen = Person(heathensQueue, heathensCounter, heathensQueue_cv, heathens_cv, States.HEATHENS_RULE,
                     States.HEATHENS_TRANSITION, "heathen")
    for i in range(NR_OF_HEATHENS):
        subscribe_thread(lambda: person_thread(heathen, prude))
    for i in range(NR_OF_PRUDES):
        subscribe_thread(lambda: person_thread(prude, heathen))