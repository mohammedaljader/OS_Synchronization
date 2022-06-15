from Environment import *


def thread_person(me, other):
    while True:
        mutex.wait()

        me.queue.v += 1
        # If the current state is not in this group`s favor or is Neutral, add person to queue
        while state.v not in (me.rule, States.NEUTRAL):
            me.cvar.wait()

        me.queue.v -= 1
        me.count.v += 1

        if state.v == States.NEUTRAL:  # Take hold of the field if the state is Neutral
            state.v = me.rule
            # If the current group currently controls the field, but the queue for the other group becomes larger
        # Change to Transition state in favor of the other group
        elif state.v == me.rule and other.queue.v > me.queue.v:
            state.v = other.transition

        mutex.signal()

        # Critical section - Crossing the field

        mutex.wait()
        me.count.v -= 1

        if me.count.v == 0:  # Last person to leave the field of this group
            if other.count.v > 0:  # If there is a queue of the other group, give the control to them
                state.v = other.rule
                other.cvar.notify_all()  # Wake up all people in the other queue
            else:
                state.v = States.NEUTRAL
        # If the current group currently controls the field, but the queue for the other group becomes larger
        # Change to Transition state in favor of the other group
        if state.v == me.rule and other.queue.v > me.queue.v:
            state.v = other.transition

        mutex.signal()


class States:
    NEUTRAL = 'neutral'
    HEATHENS_RULE = 'heathens rule'
    PRUDES_RULE = 'prudes rule'
    HEATHENS_TRANSITION = 'transition to heathens'
    PRUDES_TRANSITION = 'transition to prudes'


state = MyString(States.NEUTRAL, "state")
mutex = MyMutex("mutex")
heathen_queue = MyInt(0, "heathen count")
heathen_count = MyInt(0, "heathen in field")
prude_queue = MyInt(0, "prude count")
prude_count = MyInt(0, "prude in field")

heathen_cvar = MyConditionVariable(mutex, "heathen cond. var")
prude_cvar = MyConditionVariable(mutex, "prude cond. var")


class Person:
    def __init__(self, queue, count, cvar, rule, transition):
        self.queue = queue
        self.count = count
        self.cvar = cvar
        self.rule = rule
        self.transition = transition


def setup():
    heathen = Person(heathen_queue, heathen_count, heathen_cvar, States.HEATHENS_RULE, States.HEATHENS_TRANSITION)
    prude = Person(prude_queue, prude_count, prude_cvar, States.PRUDES_RULE, States.PRUDES_TRANSITION)

    for i in range(5):
        subscribe_thread(lambda: thread_person(heathen, prude))
        subscribe_thread(lambda: thread_person(prude, heathen))