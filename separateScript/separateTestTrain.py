import os
import random
import shutil

scriptLoc = os.path.dirname(os.path.realpath(__file__))

imgList = []
testList = []
trainList = []

for filename in os.listdir(os.path.join(scriptLoc, "imgFolder")):
    imgList.append(filename)

random.shuffle(imgList)

for i in range(int(len(imgList) * .1)):
    testList.append(imgList[i])

for i in range(int(len(imgList) * .9)):
    trainList.append(imgList[len(imgList) - i - 1])

for filename in testList:
    shutil.move(os.path.join(scriptLoc, "imgFolder", filename), os.path.join(scriptLoc, "train"))
    shutil.move(os.path.join(scriptLoc, "xmlFolder", filename[:len(filename) - 4]) + ".xml", os.path.join(scriptLoc, "train"))

for filename in trainList:
    shutil.move(os.path.join(scriptLoc, "imgFolder", filename), os.path.join(scriptLoc, "test"))
    shutil.move(os.path.join(scriptLoc, "xmlFolder", filename[:len(filename) - 4]) + ".xml", os.path.join(scriptLoc, "test"))