import couchdb
import json
import xmltodict
import os
import random

"""
Used this method of converting xml files to json files
https://www.geeksforgeeks.org/python-xml-to-json/
"""
def xmlToJson(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
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
            
def chooseTestData(dir, percentage):
    jsonList = []
    for filename in os.listdir(dir):
        jsonList.append(os.path.join(dir, filename))
    random.shuffle(jsonList)
    for x in jsonList[:int(len(jsonList) * percentage / 100)]:
        with open(x, "r+") as json_file:
            print(x)
            data = json.load(json_file)
            holdback = {'holdback': "true"}
            data.update(holdback)
            write_json(data, x)
            json_file.close()    

def uploadJsonFromDir(dir, db):

    for filename in os.listdir(dir):
        with open(dir + "/" + filename) as json_file:         
            doc = json.load(json_file)
            db.save(doc)
            json_file.close()

def main():

    couch = couchdb.Server('http://admin:password@127.0.0.1:5984')
    db = couch[DB_NAME]

    #Creates folder in this dir holding json files
    xmlToJson(DIR_TO_XMLS) 

    #Adds {holdback: true} in test data
    chooseTestData(DIR_TO_JSON_FOLDER_CREATED, 10)
    
    #Uploads Json files to DB
    uploadJsonFromDir(DIR_TO_JSON_FOLDER_CREATED, db)

if __name__ == "__main__":
    main()