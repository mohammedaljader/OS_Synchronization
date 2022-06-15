from Environment import *


def person_thread(me, other):
    while True:
        mutex.wait()

        me.queueCounter.v += 1

        while state.v == other.rule or state.v == me.transition:
            me.cv.wait()

        me.queueCounter.v -= 1
        me.counter.v += 1

        if state.v == States.NEUTRAL:
            state.v = me.rule

        elif state.v == other.rule and me.queueCounter.v > other.queueCounter.v:
            state.v = me.transition

        mutex.signal()

        print(f"walking field...{me.name}")

        mutex.wait()

        me.counter.v -= 1

        if state.v == me.rule and other.queueCounter.v > me.queueCounter.v:
            state.v = other.transition

        if state.v == other.transition and me.counter.v == 0:
            state.v = other.rule
            if other.queueCounter.v > 0:
                other.cv.notify_all()

        if state.v == me.rule and me.queueCounter.v == 0:
            state.v = States.NEUTRAL

        mutex.signal()


class States:
    NEUTRAL = "neutral"
    HEATHENS_RULE = "heathens rule"
    PRUDES_RULE = "prudes rule"
    HEATHENS_TRANSITION = "transitioning to heathens"
    PRUDES_TRANSITION = "transitioning to prudes"


class Person(object):
    def __init__(self, counter, queueCounter, cv, rule, transition, name):
        self.counter = counter
        self.queueCounter = queueCounter
        self.cv = cv
        self.rule = rule
        self.transition = transition
        self.name = name


mutex = MyMutex("mutex")

heathens_cv = MyConditionVariable(mutex, "heathens_cv")

prudes_cv = MyConditionVariable(mutex, "prudes_cv")

heathensQueue = MyInt(0, "heathensQueue")
heathensCount = MyInt(0, "heathensCount")

prudesQueue = MyInt(0, "prudesQueue")
prudesCount = MyInt(0, "prudesCount")

state = MyString(States.NEUTRAL, "state")


def setup():
    prude = Person(prudesCount, prudesQueue, prudes_cv, States.PRUDES_RULE,
                   States.PRUDES_TRANSITION, "prude")
    heathen = Person(heathensCount, heathensQueue, heathens_cv, States.HEATHENS_RULE,
                     States.HEATHENS_TRANSITION, "heathen")
    for i in range(5):
        subscribe_thread(lambda: person_thread(heathen, prude))
    for i in range(5):
        subscribe_thread(lambda: person_thread(prude, heathen))
