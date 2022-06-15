from Environment import *


def person_thread(me, other):
    while True:
        mutex.wait()

        me.buffer_counter.v += 1

        while state.v == other.transition:
            me.buffer_cv.wait()

        me.buffer_counter.v -= 1

        me.queue_counter.v += 1

        if state.v == States.NEUTRAL:
            state.v = me.rule

        elif state.v == other.rule and me.queue_counter.v > other.queue_counter.v:
            state.v = me.transition

        while state.v == other.rule or state.v == me.transition:
            me.queue_cv.wait()

        mutex.signal()

        print("walking field...")

        mutex.wait()

        me.queue_counter.v -= 1

        if state.v == me.rule and other.queue_counter.v > me.queue_counter.v:
            state.v = other.transition

        if state.v == other.transition and me.queue_counter.v == 0:
            state.v = other.rule
            if other.queue_counter.v > 0:
                other.queue_cv.notify_all()
            if me.buffer_counter.v > 0:
                me.buffer_cv.notify_all()

        if state.v == me.rule and me.queue_counter.v == 0:
            state.v = States.NEUTRAL

        mutex.signal()


class States:
    NEUTRAL = "neutral"
    HEATHENS_RULE = "heathens rule"
    PRUDES_RULE = "prudes rule"
    HEATHENS_TRANSITION = "transitioning to heathens"
    PRUDES_TRANSITION = "transitioning to prudes"


class Person(object):
    def __init__(self, buffer_counter, queue_counter, buffer_cv, queue_cv, rule, transition):
        self.buffer_counter = buffer_counter
        self.queue_counter = queue_counter
        self.buffer_cv = buffer_cv
        self.queue_cv = queue_cv
        self.rule = rule
        self.transition = transition


mutex = MyMutex("mutex")

heathens_buffer_cv = MyConditionVariable(mutex, "heathens_buffer")
heathens_queue_cv = MyConditionVariable(mutex, "heathens_queue")

prudes_buffer_cv = MyConditionVariable(mutex, "prudes_buffer")
prudes_queue_cv = MyConditionVariable(mutex, "prudes_queue")

heathens_in_buffer = MyInt(0, "heathens_in_buffer")
prudes_in_buffer = MyInt(0, "prudes_in_buffer")

heathens_in_queue = MyInt(0, "heathens_in_queue")
prudes_in_queue = MyInt(0, "prudes_in_queue")

state = MyString(States.NEUTRAL, "state")


def setup():
    prude = Person(prudes_in_buffer, prudes_in_queue, prudes_buffer_cv, prudes_queue_cv, States.PRUDES_RULE,
                   States.PRUDES_TRANSITION)
    heathen = Person(heathens_in_buffer, heathens_in_queue, heathens_buffer_cv, heathens_queue_cv, States.HEATHENS_RULE,
                     States.HEATHENS_TRANSITION)
    for i in range(5):
        subscribe_thread(lambda: person_thread(heathen, prude))
        subscribe_thread(lambda: person_thread(prude, heathen))
