from Environment import *


def prepareFood(i):
    arr = ["Carnivore", "Vegetarian"]
    if arr.__contains__(i):
        return i


def vegetarianCookThread():
    while True:
        mutex.wait()
        while bag.contains(prepareFood("Vegetarian")):
            cv_vegetarian_cook.wait()

        while bag.size() < bagCapacity:
            bag.put(prepareFood("Vegetarian"))

        print("prepareFoodForVegetarian()")
        cv_vegetarian_savage.notify_all()
        print("Call all Vegetarian to come to eat!! ")
        mutex.signal()


def vegetarianSavagesThread():
    while True:
        mutex.wait()
        while not bag.contains(prepareFood("Vegetarian")):
            cv_vegetarian_savage.wait()

        print("vegetarianEat()")
        bag.get(prepareFood("Vegetarian"))

        if not bag.contains(prepareFood("Vegetarian")):
            cv_vegetarian_cook.notify()
            print("No Food available for vegetarian!")
        mutex.signal()


def carnivoreCookThread():
    while True:
        mutex.wait()
        while bag.contains(prepareFood("Carnivore")):
            cv_carnivore_cook.wait()

        while bag.size() < bagCapacity:
            bag.put(prepareFood("Carnivore"))

        print("prepareFoodForCarnivore()")
        cv_carnivore_savage.notify_all()
        print("Call all carnivore to come to eat!")
        mutex.signal()


def carnivoreSavagesThread():
    while True:
        mutex.wait()
        while not bag.contains(prepareFood("Carnivore")):
            cv_carnivore_savage.wait()

        print("CarnivoreEat()")
        bag.get(prepareFood("Carnivore"))

        if not bag.contains(prepareFood("Carnivore")):
            cv_carnivore_cook.notify()
            print("No Food available for carnivores!")
        mutex.signal()


bagCapacity = 6
bag = MyBag(bagCapacity, "storage")
mutex = MyMutex("mutex")

cv_carnivore_savage = MyConditionVariable(mutex, 'cv_carnivore_savage')
cv_vegetarian_savage = MyConditionVariable(mutex, "cv_vegetarian_savage")
cv_carnivore_cook = MyConditionVariable(mutex, 'cv_carnivore_cook')
cv_vegetarian_cook = MyConditionVariable(mutex, "cv_vegetarian_cook")


def setup():
    subscribe_thread(vegetarianCookThread)
    subscribe_thread(carnivoreCookThread)
    for i in range(10):
        subscribe_thread(vegetarianSavagesThread)
    for i in range(6):
        subscribe_thread(carnivoreSavagesThread)
