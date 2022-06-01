# DinningPhilosopher
from Environment import *

forks = [MySemaphore(1, f"Sem{i}") for i in range(5)]


def left(i):
    return i


def right(i):
    return (i + 1) % 5


def think(i):
    print(f"{i} is thinking!")


def eat(i):
    print(f"{i} is eating!")


def get_fork(i):
    while True:
        think(i)
        forks[left(i)].wait()
        forks[right(i)].wait()
        eat(i)
        forks[left(i)].signal()
        forks[right(i)].signal()


def put_fork(i):
    while True:
        think(i)
        forks[right(i)].wait()
        forks[left(i)].wait()
        eat(i)
        forks[right(i)].signal()
        forks[left(i)].signal()


def setup():
    for i in range(len(forks)):
        subscribe_thread(lambda: get_fork(i))
        subscribe_thread(lambda: put_fork(i))
