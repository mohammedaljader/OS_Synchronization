from Environment import *

bag = MyBag(6, "storage")
mutex = MyMutex("mutex")

cv_carnivore_savage = MyConditionVariable(mutex, 'cv_carnivore_savage')
cv_vegetarian_savage = MyConditionVariable(mutex, "cv_vegetarian_savage")
cv_carnivore_cook = MyConditionVariable(mutex, 'cv_carnivore_cook')
cv_vegetarian_cook = MyConditionVariable(mutex, "cv_vegetarian_cook")

carnivore_savage = MyInt(0, "carnivore_savage")
vegetarian_savage = MyInt(0, "vegetarian_savage")
carnivore_cook = MyInt(0, "carnivore_cook")
vegetarian_cook = MyInt(0, "vegetarian_cook")


# def thread_cook():
#     while True:

