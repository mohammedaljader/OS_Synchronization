from Environment import *


def person_thread(me, other):
    while True:
        mutex.wait()

        me.turnCounter.v += 1

        while state.v == other.transition:
            me.turn_cv.wait()

        me.turnCounter.v -= 1

        me.queueCounter.v += 1

        if state.v == States.NEUTRAL:
            state.v = me.rule

        elif state.v == other.rule and me.queueCounter.v > other.queueCounter.v:
            state.v = me.transition

        while state.v == other.rule or state.v == me.transition:
            me.queue_cv.wait()

        mutex.signal()

        print(f"walking field...{me.name}")

        mutex.wait()

        me.queueCounter.v -= 1

        if state.v == me.rule and other.queueCounter.v > me.queueCounter.v:
            state.v = other.transition

        if state.v == other.transition and me.queueCounter.v == 0:
            state.v = other.rule
            if other.queueCounter.v > 0:
                other.queue_cv.notify_all()
            if me.turnCounter.v > 0:
                me.turn_cv.notify_all()

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
    def __init__(self, turnCounter, queueCounter, buffer_cv, queue_cv, rule, transition, name):
        self.turnCounter = turnCounter
        self.queueCounter = queueCounter
        self.turn_cv = buffer_cv
        self.queue_cv = queue_cv
        self.rule = rule
        self.transition = transition
        self.name = name


mutex = MyMutex("mutex")

heathensTurn_cv = MyConditionVariable(mutex, "heathensTurn_cv")
heathensQueue_cv = MyConditionVariable(mutex, "heathensQueue_cv")

prudesTurn_cv = MyConditionVariable(mutex, "prudesTurn_cv")
prudesQueue_cv = MyConditionVariable(mutex, "prudesQueue_cv")

heathensTurn = MyInt(0, "heathensTurn")
prudesTurn = MyInt(0, "prudesTurn")

heathensQueue = MyInt(0, "heathensQueue")
prudesQueue = MyInt(0, "prudesQueue")

state = MyString(States.NEUTRAL, "state")


def setup():
    prude = Person(prudesTurn, prudesQueue, prudesTurn_cv, prudesQueue_cv, States.PRUDES_RULE,
                   States.PRUDES_TRANSITION, "prude")
    heathen = Person(heathensTurn, heathensQueue, heathensTurn_cv, heathensQueue_cv, States.HEATHENS_RULE,
                     States.HEATHENS_TRANSITION, "heathen")
    for i in range(5):
        subscribe_thread(lambda: person_thread(heathen, prude))
    for i in range(5):
        subscribe_thread(lambda: person_thread(prude, heathen))