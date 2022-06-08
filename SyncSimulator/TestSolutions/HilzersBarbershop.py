# HilzersBarbershop
from Environment import *

n = 20
customers = MyInt(0, "customers")
mutex = MySemaphore(1, "mutex")
sofa = MySemaphore(4, "SofaMultiplex")
customer1 = MySemaphore(0, "customer1")
customer2 = MySemaphore(0, "customer2")
barber = MySemaphore(0, "barber")
payment = MySemaphore(0, "payment")
receipt = MySemaphore(0, "receipt")
queue1 = []
queue2 = []


def customerThread():
    sem1 = MySemaphore(0, "sem1")
    sem2 = MySemaphore(0, "sem2")

    mutex.wait()
    if customers.v == n:
        mutex.signal()
        print("Balk")
    customers.v += 1
    queue1.append(sem1)
    mutex.signal()

    # enterShop
    customer1.signal()
    sem1.wait()

    sofa.wait()
    print("SitOnSofa")
    sem1.signal()
    mutex.wait()
    queue2.append(sem2)
    mutex.signal()
    customer2.signal()
    sem2.wait()
    sofa.signal()

    print("sitInBarberChair()")

    payment.signal()
    receipt.wait()
    mutex.wait()
    customers.v -= 1
    mutex.signal()


def barberThread():
    customer1.wait()
    mutex.wait()
    sem = queue1.pop(0)
    sem.signal()
    sem.wait()
    mutex.signal()
    sem.signal()

    customer2.wait()
    mutex.wait()
    sem = queue2.pop(0)
    mutex.signal()
    sem.signal()

    barber.signal()
    print("cutHair()")

    payment.wait()
    print("acceptPayment()")
    receipt.signal()


def setup():
    subscribe_thread(barberThread)
    subscribe_thread(customerThread)
