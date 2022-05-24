from Environment import *

mutex = MyMutex(1)
leaderQueue = MySemaphore(0, "leaderQueue")
followerQueue = MySemaphore(0, "followerQueue")
rendezvous = MySemaphore(0, "rendezvous")
count = MyInt(0, "count")
followers = MyInt(0, "followers")
leaders = MyInt(0, "leaders")


def leadersThread():
    mutex.wait()
    if followers.v > 0:
        followers.v -= 1
        followerQueue.signal()
    else:
        leaders.v += 1
        mutex.signal()
        leaderQueue.wait()

    print("dance {leaders}")

    rendezvous.wait()
    mutex.signal()


def followersThread():
    mutex.wait()
    if leaders.v > 0:
        leaders.v -= 1
        leaderQueue.signal()
    else:
        followers.v += 1
        mutex.signal()
        followerQueue.wait()

    print("dance {followers}")
    rendezvous.signal()


def setup():
    subscribe_thread(followersThread)
    subscribe_thread(leadersThread)
