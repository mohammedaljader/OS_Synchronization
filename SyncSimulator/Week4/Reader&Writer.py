from Environment import *


def reader_thread():
    while True:
        mutex.wait()
        while active_writers.v > 0 or waiting_writers.v > 0:  # check if safe to read if any writers, wait
            waiting_readers.v += 1
            cv_reader.wait()
            waiting_readers.v -= 1
        active_readers.v += 1
        mutex.signal()

        print("read()")

        mutex.wait()
        active_readers.v -= 1
        if active_readers.v == 0 and waiting_writers.v > 0:  # if no other readers still active, wake up writer
            cv_writer.notify()
        mutex.signal()


def writer_thread():
    while True:
        mutex.wait()
        while active_writers.v > 0 or active_readers.v > 0:  # check if safe to write, if any readers or writers,wait
            waiting_writers.v += 1
            cv_writer.wait()
            waiting_writers.v -= 1
        active_writers.v += 1
        mutex.signal()

        print("write()")

        mutex.wait()
        active_writers.v -= 1
        if waiting_writers.v > 0:  # give priority to other writers
            cv_writer.notify()
        elif waiting_readers.v > 0:
            cv_reader.notify()
        mutex.signal()


mutex = MyMutex("mutex")
cv_reader = MyConditionVariable(mutex, "cv_reader")
cv_writer = MyConditionVariable(mutex, "cv_writer")
active_readers = MyInt(0, "active_readers")
active_writers = MyInt(0, "active_writers")
waiting_readers = MyInt(0, "waiting_readers")
waiting_writers = MyInt(0, "waiting_writers")


def setup():
    for i in range(7):
        subscribe_thread(reader_thread)
    for i in range(4):
        subscribe_thread(writer_thread)
