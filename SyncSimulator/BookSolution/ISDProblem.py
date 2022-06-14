# ISDProblem
from Environment import *

insertMutex = MyMutex("insertMutex")
noSearcher = MySemaphore(1, "noSearcher")
noInserter = MySemaphore(1, "noInserter")
searchSwitch = MyLightswitch(noSearcher, "searchSwitch")
insertSwitch = MyLightswitch(noInserter, "insertSwitch")


def Searcher():
    while True:
        searchSwitch.lock(noSearcher)
        print("Search()")
        searchSwitch.unlock(noSearcher)


def Inserter():
    while True:
        insertSwitch.lock(noInserter)
        insertMutex.wait()
        print("Wait()")
        insertMutex.signal()
        insertSwitch.unlock(noInserter)


def Deleter():
    while True:
        noSearcher.wait()
        noInserter.wait()
        print("Delete()")
        noSearcher.signal()
        noInserter.signal()


def setup():
    subscribe_thread(Searcher)
    subscribe_thread(Inserter)
    subscribe_thread(Deleter)
