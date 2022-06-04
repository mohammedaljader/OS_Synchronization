from Environment import *

x = 0


def myThreadA():
    global x
    for i in range(100):
        x += 1
        print(f"1: {x}")


def myThreadB():
    global x
    for i in range(100):
        x += 1
        print(f"2: {x}")


def setup():
    subscribe_thread(myThreadA)
    subscribe_thread(myThreadB)
