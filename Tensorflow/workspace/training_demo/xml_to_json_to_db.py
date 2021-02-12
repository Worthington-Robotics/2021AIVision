"""
----------------------------------------------------------------------------
Authors:     FRC Team 4145
Description: This script takes the xml files created from labelImg and puts
             them into a database as a json. It also changes the xml files 
             created through labelImg to be relative to your computer.
Comments:    Follow https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html
             After you compile all your test/train data and put them in their
             respective 
----------------------------------------------------------------------------
"""

import couchdb
import json
import xmltodict
import os
import random
import shutil
import xml.etree.ElementTree as ET

"""
Used this method of converting xml files to json files
https://www.geeksforgeeks.org/python-xml-to-json/
"""
def xmlToJson(directory):
    for filename in os.listdir(directory):
        xml = os.path.join(directory, filename)
        with open(xml) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
            xml_file.close()

        json_data = json.dumps(data_dict)

        (file, ext) = os.path.splitext(filename)
            
        with open("json/" + file + ".json", "w") as json_file:
            json_file.write(json_data)
            json_file.close() 
            

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)  
        f.close()

def changeXmlPaths(directory, imgDir, folder):
    for filename in os.listdir(directory):
        xml = os.path.join(directory, filename)
        if(xml.endswith(".xml")):
            with open(xml) as xml_file:
                xmlTree = ET.parse(xml_file)
                (file, ext) = os.path.splitext(filename)
                xmlTree.find("path").text = os.path.join(imgDir, file) + ".jpg"
                xmlTree.find("folder").text = folder
                xmlTree.write(xml)
            
def chooseTestData(dir, percentage, imgFolder):
    jsonList = []
    for filename in os.listdir(dir):
        jsonList.append(os.path.join(dir, filename))
    random.shuffle(jsonList)
    for filepath in jsonList[:int(len(jsonList) * percentage / 100)]:
        
        with open(filepath, "r+") as json_file:
            print(filepath)
            data = json.load(json_file)
            holdback = {'holdback': "true"}
            filename = data['annotation']['filename']
            imgLoc = imgFolder + filename
            data.update(holdback)
            data['annotation']['path'] = imgLoc

            write_json(data, filepath)
            json_file.close()

def uploadJsonFromDir(dir, db):

    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename)) as json_file:         
            doc = json.load(json_file)
            db.save(doc)
            json_file.close()

def separateTrainTestData(testDir, trainDir, jsonDir, xmlDir, imgDir):
    for filename in os.listdir(jsonDir):
        with open(os.path.join(jsonDir, filename), "r+") as json_file:
            data = json.load(json_file)
            (file, ext) = os.path.splitext(filename)
            if(data.get('holdback') == 'true'):
                #shutil.move(os.path.join(xmlDir, file) + '.xml', testDir)
                #shutil.move(os.path.join(imgDir, file) + '.jpg', testDir)
                shutil.move(xmlDir + "/" + file + '.xml', testDir)
                shutil.move(imgDir + "/" + file + '.jpg', testDir)
                #os.rename(xmlDir + "/" + data['annotation'] ['filename'][:len(filename) - 5] + '.xml', testDir + data['annotation'] ['filename'][:len(filename) - 5] + '.xml')
            else:
                #shutil.move(os.path.join(xmlDir, file, '.xml'), trainDir)
                #shutil.move(os.path.join(imgDir, file, '.jpg'), trainDir)
                shutil.move(xmlDir + "/" + file + '.xml', trainDir)
                shutil.move(imgDir + "/" + file + '.jpg', trainDir)
                #os.rename(xmlDir + "/" + data['annotation'] ['filename'][:len(filename) - 5] + '.xml', trainDir + data['annotation'] ['filename'][:len(filename) - 5] + '.xml')
        

def main():

    scriptLoc = os.path.dirname(os.path.realpath(__file__))
    PATH_TO_XMLS = os.path.join(scriptLoc, "images", "Directories")
    PATH_TO_JSON_FOLDER = os.path.join(scriptLoc, "json")
    PATH_TO_IMAGE_FOLDER = os.path.join(scriptLoc, "images")
    PATH_TO_TEST_IMAGE_FOLDER = os.path.join(scriptLoc, "images", "test")
    PATH_TO_TRAIN_IMAGE_FOLDER = os.path.join(scriptLoc, "images", "train")

    #Should be the name you assigned the database. For me, I named it 'ai-test'
    DB_NAME = ""

    #Comment out if you aren't using db
    #couch = couchdb.Server('http://admin:password@127.0.0.1:5984')
    #db = couch[DB_NAME]

    #Creates folder in this dir holding json files
    xmlToJson(PATH_TO_XMLS) 

    #Adds {holdback: true} in test data, create json folder inside folder within this program
    chooseTestData(PATH_TO_JSON_FOLDER, 10, PATH_TO_IMAGE_FOLDER)

    #The test and traing image folders should be created within the image folder inside the "training_demo" folder
    separateTrainTestData(PATH_TO_TEST_IMAGE_FOLDER, PATH_TO_TRAIN_IMAGE_FOLDER, PATH_TO_JSON_FOLDER, PATH_TO_XMLS, PATH_TO_IMAGE_FOLDER)

    #Allows bounding boxes to be done of different computers
    changeXmlPaths(PATH_TO_TEST_IMAGE_FOLDER, PATH_TO_TEST_IMAGE_FOLDER, "test")
    changeXmlPaths(PATH_TO_TRAIN_IMAGE_FOLDER, PATH_TO_TRAIN_IMAGE_FOLDER, "train")

    #Uploads Json files to DB, Comment out if you aren't using a db
    #uploadJsonFromDir(PATH_TO_JSON_FOLDER, db)
if __name__ == "__main__":
    main()
