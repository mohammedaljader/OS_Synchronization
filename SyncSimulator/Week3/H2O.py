from Environment import *

N = 7

hPipet = MySemaphore(2, "hPipet")
oPipet = MySemaphore(1, "oPipet")
hTurnstile = MySemaphore(0, "hTurnstile")
oTurnstile = MySemaphore(0, "oTurnstile")


def OxygenThread():
    while True:
        oPipet.wait()

        hTurnstile.signal(2)

        oTurnstile.wait()
        oTurnstile.wait()

        print("O")

        oPipet.signal()


def HydrogenThread():
    while True:
        hPipet.wait()

        hTurnstile.wait()

        print("H")

        oTurnstile.signal()
        hPipet.signal()


def setup():
    for i in range(N):
        subscribe_thread(HydrogenThread)
        subscribe_thread(OxygenThread)
