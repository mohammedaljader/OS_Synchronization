from Environment import *

N = 5
forks = [True for i in range(N)]
mutex = MyMutex("mutex")
condition_variables = [MyConditionVariable(mutex, f"condition{i}") for i in range(N)]


def philosopher_thread(i):
    while True:
        print("think()")
        mutex.wait()
        while not is_Available(i):
            condition_variables[i].wait()

        forks[left(i)] = False
        forks[right(i)] = False
        mutex.signal()

        print("eat()")

        mutex.wait()
        forks[left(i)] = True
        forks[right(i)] = True
        condition_variables[left(i)].notify()
        condition_variables[right(i)].notify()
        mutex.signal()


def left(i):
    return i


def right(i):
    return (i + 1) % N


def is_Available(i):
    if forks[left(i)] and forks[right(i)]:
        return True


def setup():
    subscribe_thread(lambda: philosopher_thread(0))
    subscribe_thread(lambda: philosopher_thread(1))
    subscribe_thread(lambda: philosopher_thread(2))
    subscribe_thread(lambda: philosopher_thread(3))
    subscribe_thread(lambda: philosopher_thread(4))
