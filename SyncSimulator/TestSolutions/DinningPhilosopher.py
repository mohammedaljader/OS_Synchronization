# DinningPhilosopher
from Environment import *

forks = [MySemaphore(1, f"Sem{i}") for i in range(5)]
footman = MySemaphore(1, "footman")


def left(i):
    return i


def right(i):
    return (i + 1) % 5


def get_fork(i):
    while True:
        footman.wait()
        forks[right(i)].wait()
        forks[left(i)].wait()


def put_fork(i):
    while True:
        forks[right(i)].signal()
        forks[left(i)].signal()
        footman.signal()


def setup():
    for i in range(len(forks)):
        subscribe_thread(lambda: get_fork(i))
        subscribe_thread(lambda: put_fork(i))
