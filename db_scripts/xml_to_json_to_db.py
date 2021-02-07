import couchdb
import json
import xmltodict
import os
import random
import shutil

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

            with open("json/" + filename[0: len(filename) - 4] + ".json", "w") as json_file:
                json_file.write(json_data)
                json_file.close() 

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)  
        f.close()
            
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
        with open(dir + "/" + filename) as json_file:         
            doc = json.load(json_file)
            db.save(doc)
            json_file.close()

def separateTrainTestData(testDir, trainDir, jsonDir, xmlDir, imgDir):
    for filename in os.listdir(jsonDir):
        with open(jsonDir + "/" + filename, "r+") as json_file:
            data = json.load(json_file)
            if(data.get('holdback') == 'true'):
                shutil.move(xmlDir + "/" + filename[:len(filename) - 5] + '.xml', testDir)
                shutil.move(imgDir + "/" + filename[:len(filename) - 5] + '.jpg', testDir)
                #os.rename(xmlDir + "/" + data['annotation'] ['filename'][:len(filename) - 5] + '.xml', testDir + data['annotation'] ['filename'][:len(filename) - 5] + '.xml')
            else:
                shutil.move(xmlDir + "/" + filename[:len(filename) - 5] + '.xml', trainDir)
                shutil.move(imgDir + "/" + filename[:len(filename) - 5] + '.jpg', trainDir)
                #os.rename(xmlDir + "/" + data['annotation'] ['filename'][:len(filename) - 5] + '.xml', trainDir + data['annotation'] ['filename'][:len(filename) - 5] + '.xml')
        

def main():

    #Comment out if you aren't using db
    couch = couchdb.Server('http://admin:password@127.0.0.1:5984')
    db = couch[DB_NAME]

    #Creates folder in this dir holding json files
    xmlToJson(PATH_TO_XMLS) 

    #Adds {holdback: true} in test data, create json folder inside folder within this program
    chooseTestData(PATH_TO_JSON_FOLDER_CREATED, 10, PATH_TO_IMG_FOLDER)

    #The test and traing image folders should be created within the image folder inside the "training_demo" folder
    separateTrainTestData(PATH_TO_TEST_IMAGE_FOLDER, PATH_TO_TRAIN_IMAGE_FOLDER, PATH_TO_JSON_FOLDER, PATH_TO_XML_FOLDER, PATH_TO_IMAGE_FOLDER)
    
    #Uploads Json files to DB, Comment out if you aren't using a db
    uploadJsonFromDir(PATH_TO_JSON_FOLDER, db)
if __name__ == "__main__":
    main()
