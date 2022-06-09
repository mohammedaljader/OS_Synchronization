from Environment import *


def reader_thread():
    while True:
        mutex.wait()
        while active_writers.v > 0 or (waiting_writers.v > 0 and priority.v):
            waiting_readers.v += 1
            cv_reader.wait()
            waiting_readers.v -= 1
        active_readers.v += 1
        mutex.signal()

        print("read()")

        mutex.wait()
        active_readers.v -= 1
        if active_readers.v == 0 and (
                (priority.v and waiting_writers.v > 0) or (waiting_writers.v > 0 and waiting_readers.v == 0)):
            cv_writer.notify()
        mutex.signal()


def writer_thread():
    while True:
        mutex.wait()
        while active_readers.v > 0 or active_writers.v > 0 or (waiting_readers.v > 0 and not priority.v):
            waiting_writers.v += 1
            cv_writer.wait()
            waiting_writers.v -= 1
        active_writers.v += 1
        mutex.signal()

        print("write()")

        mutex.wait()
        active_writers.v -= 1
        if waiting_readers.v > 0 and not priority.v:
            cv_reader.notify_all()
        elif waiting_writers.v > 0:
            cv_writer.notify()
        mutex.signal()


mutex = MyMutex("mutex")
cv_reader = MyConditionVariable(mutex, "cv_reader")
cv_writer = MyConditionVariable(mutex, "cv_writer")
active_readers = MyInt(0, "active_readers")
active_writers = MyInt(0, "active_writers")
waiting_readers = MyInt(0, "waiting_readers")
waiting_writers = MyInt(0, "waiting_writers")
priority = MyBool(True, "priority")


def setup():
    for i in range(7):
        subscribe_thread(reader_thread)
    for i in range(7):
        subscribe_thread(writer_thread)


# While and if statement

# if a = 72  -> 1
#    cv.notifyAll

# while not(a == 72)  -> 2
#      cv.wait()
#      a =42

# while not(a == 72)
#      cv.wait()

