# BaboonCrossing
from Environment import *

empty = MySemaphore(1, "empty")
left_switch = MyLightswitch(empty)
right_switch = MyLightswitch(empty)
left_multiplex = MySemaphore(5, "left_multiplex")
right_multiplex = MySemaphore(5, "right_multiplex")
turnstile = MySemaphore(1, "turnstile")


def left_baboon():
    while True:
        turnstile.wait()
        left_switch.lock(empty)
        turnstile.signal()

        left_multiplex.wait()
        print('-> left baboon got on to the rope.')
        left_multiplex.signal()
        print('-> left baboon got off to the rope.')
        left_switch.unlock(empty)


def right_baboon():
    while True:
        turnstile.wait()
        right_switch.lock(empty)
        turnstile.signal()

        right_multiplex.wait()
        print('-> right baboon got on to the rope.')
        right_multiplex.signal()
        print('-> left baboon got off to the rope.')
        right_switch.unlock(empty)


def setup():
    subscribe_thread(left_baboon)
    subscribe_thread(right_baboon)
