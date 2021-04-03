import os
import random
import shutil

scriptLoc = os.path.dirname(os.path.realpath(__file__))

imgFolder = os.path.join(scriptLoc, "images", "all_images")
xmlFolder = os.path.join(scriptLoc, "images", "all_directories")
trainFolder = os.path.join(scriptLoc, "images", "test")
testfolder = os.path.join(scriptLoc, "images", "train")

imgList = []
testList = []
trainList = []

for filename in os.listdir(imgFolder):
    imgList.append(filename)

random.shuffle(imgList)

for i in range(int(len(imgList) * .1)):
    testList.append(imgList[i])

for i in range(int(len(imgList) * .9)):
    trainList.append(imgList[len(imgList) - i - 1])

for filename in testList:
    shutil.move(os.path.join(imgFolder, filename), trainFolder)
    shutil.move(os.path.join(xmlFolder, filename[:len(filename) - 4]) + ".xml", trainFolder)

for filename in trainList:
    shutil.move(os.path.join(imgFolder, filename), testfolder)
    shutil.move(os.path.join(xmlFolder, filename[:len(filename) - 4]) + ".xml", testfolder)