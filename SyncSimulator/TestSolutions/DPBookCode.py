# DPBookCode
from Environment import *

forks = [MySemaphore(0, f"Sem{i}") for i in range(5)]
mutex = MyMutex(1)
state = ['thinking'] * 5


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
        mutex.wait()
        state[i] = 'hungry'
        test(i)
        mutex.signal()
        forks[i].wait()


def put_fork(i):
    while True:
        mutex.wait()
        state[i] = 'thinking'
        test(right(i))
        test(left(i))
        mutex.signal()


def test(i):
    if state[i] == 'hungry' and state[left(i)] != 'eating' and state[right(i)] != 'eating':
        state[i] = 'eating'
        forks[i].signal()


def setup():
    for i in range(len(forks)):
        think(i)
        subscribe_thread(lambda: get_fork(i))
        eat(i)
        subscribe_thread(lambda: put_fork(i))