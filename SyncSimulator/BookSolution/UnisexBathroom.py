# UnisexBathroom
from Environment import *

empty = MySemaphore(1, "empty")
maleSwitch = MyLightswitch(empty)
femaleSwitch = MyLightswitch(empty)
maleMultiplex = MySemaphore(3, "maleMultiplex")
femaleMultiplex = MySemaphore(3, "femaleMultiplex")
turnstile = MySemaphore(1, "turnStile")


def Female():
    while True:
        turnstile.wait()
        femaleSwitch.lock(empty)
        turnstile.signal()
        femaleMultiplex.wait()
        print("Female at the bathroom!")
        femaleMultiplex.signal()
        femaleSwitch.unlock(empty)

def Male():
    while True:
        turnstile.wait()
        maleSwitch.lock(empty)
        turnstile.signal()
        maleMultiplex.wait()
        print("Male at the bathroom!")
        maleMultiplex.signal()
        maleSwitch.unlock(empty)


def setup():
    subscribe_thread(Female)
    subscribe_thread(Male)
