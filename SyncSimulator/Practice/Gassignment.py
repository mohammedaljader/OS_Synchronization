from Environment import *

NROF_CITIZENS = 5
CONTAINER_MAX_CAPACITY = 10
actual_container_content = MyInt(0)

mutex = MyMutex("mutex")
citizen_cv = MyConditionVariable(mutex, "citizen_cv")
garbage_cleaner = MyConditionVariable(mutex, "garbage_cleaner")


def thread_citizen():
    while True:
        mutex.wait()

        while actual_container_content.v > CONTAINER_MAX_CAPACITY:
            citizen_cv.wait()

        # put_sack_in_container
        actual_container_content.v += 1
        print("actual_container_content ")

        if actual_container_content.v == CONTAINER_MAX_CAPACITY:
            garbage_cleaner.notify()

        mutex.signal()


def thread_garbage_cleaner():
    while True:
        mutex.wait()

        while actual_container_content.v < CONTAINER_MAX_CAPACITY:
            garbage_cleaner.wait()

        # empty_container
        actual_container_content.v = 0
        print("garbage_cleaner coming")

        citizen_cv.notify_all()

        mutex.signal()


def setup():
    subscribe_thread(thread_garbage_cleaner)
    for i in range(NROF_CITIZENS):
        subscribe_thread(thread_citizen)
