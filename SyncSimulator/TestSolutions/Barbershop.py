# Barbershop

from Environment import *

n = 4
customers = MyInt(0, "customers")
mutex = MyMutex("mutex")
customer = MySemaphore(0, "customer")
barber = MySemaphore(0, "barber")
customerDone = MySemaphore(0, "customerDone")
barberDone = MySemaphore(0, "barberDone")


def customerThread():
    mutex.wait()
    if customers.v == n:
        print("balk()")
    customers.v += 1
    mutex.signal()

    customer.signal()
    barber.wait()
    print("getHairCut()")
    customerDone.signal()
    barberDone.wait()

    mutex.wait()
    customers.v -= 1
    mutex.signal()


def barberThread():
    while True:
        customer.wait()
        barber.signal()
        print("cutHair()")
        customerDone.wait()
        barberDone.signal()


def setup():
    subscribe_thread(barberThread)
    for i in range(6):
        subscribe_thread(customerThread)
