# FIFOBarbershop

from Environment import *

n = 4
customers = MyInt(0, "customers")
mutex = MySemaphore(1, "mutex")
# multiplex = MySemaphore(4, "Multiplex")
customer = MySemaphore(0, "customer")
barber = MySemaphore(0, "barber")
customerDone = MySemaphore(0, "customerDone")
barberDone = MySemaphore(0, "barberDone")
queue = []


def customerThread():
    sem = MySemaphore(0)
    # multiplex.wait()
    mutex.wait()
    if customers.v == n:
        print("balk()")
    customers.v += 1
    queue.append(sem)
    mutex.signal()
    customer.signal()
    sem.wait()
    print("getHairCut()")
    customerDone.signal()
    barberDone.wait()
    mutex.wait()
    customers.v -= 1
    mutex.signal()
    # multiplex.signal()


def barberThread():
    while True:
        customer.wait()
        mutex.wait()
        sem = queue.pop(0)
        mutex.signal()
        sem.signal()
        print("cutHair()")
        customerDone.wait()
        barberDone.signal()


def setup():
    subscribe_thread(barberThread)
    for i in range(5):
        subscribe_thread(customerThread)
