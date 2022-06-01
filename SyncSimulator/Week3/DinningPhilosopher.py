# DinningPhilosopher
from Environment import *

forks = [MySemaphore(1, f"Sem{i}") for i in range(5)]


def left(i):
    return i


def right(i):
    return (i + 1) % 5


def right_handed(i):
    while True:
        print("think")
        forks[right(i)].wait()
        forks[left(i)].wait()
        print("eat")
        forks[right(i)].signal()
        forks[left(i)].signal()


def left_handed(i):
    while True:
        print("think")
        forks[left(i)].wait()
        forks[right(i)].wait()
        print("eat")
        forks[left(i)].signal()
        forks[right(i)].signal()


def philosopher(i):
    left_handed(i)
    right_handed(i)


def setup():
    for i in range(len(forks)):
        subscribe_thread(lambda: philosopher(i))
