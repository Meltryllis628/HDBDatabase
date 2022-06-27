import sqlite3
import json
from osgeo import ogr
import pandas as pd

def getDataFromGDBFile(filepath,filename = "New File"):
    """This Function takes GDB file as input. It would create a json file and returns a Dataframe"""
    driver = ogr.GetDriverByName('OpenFileGDB')
    data_source = driver.Open(filepath, 0)
    with open(filename+".json",'w+') as file:
        features = []
        for index in range(data_source.GetLayerCount()):
            layer = data_source.GetLayer(index)
            for feature in layer:
                fields = {}
                keys = feature.keys()
                for key in keys:
                    fields[key] = feature.GetField(key)
                features.append(fields)
        df = pd.DataFrame(features)
        json.dump(features,file)
        return(df)

def getDataFromJsonFile(filepath):
    """This Function takes json file as input and returns a Dataframe"""
    file = open(filepath,'rb')
    try:
        content = file.read() 
        features = json.loads(content)
        df = pd.DataFrame(features)
        return(df)
    finally:
        file.close()

def initDataBase(filename = "database.db"):
    """This Function creates new database"""
    coon = sqlite3.connect(filename)
    print("Connected")
    c = coon.cursor()
    try:
        c.execute("DROP TABLE BUILDINGS")
    except:
        pass
    c.execute('''CREATE TABLE BUILDINGS
        (ID             INT     PRIMARY KEY NOT NULL,
        USER            TEXT    ,
        BLOCK           TEXT    NOT NULL,
        POSTALCODE      INT     NOT NULL,
        STREET          TEXT    NOT NULL,
        LEVEL           INT     NOT NULL,
        UNIT            INT     NOT NULL);''')
    print("Created")
    coon.commit()
    print("Commited")
    coon.close()
    print("Closed")

def addingData(user,df,filename = "database.db"):
    """This Function adds data into database from Dataframe"""
    coon = sqlite3.connect(filename)
    print("Connected")
    c = coon.cursor()
    dataSize = df.shape[0]
    columns = ['Block', 'PostalCode', 'Street', 'Level', 'Unit']
    prefixOfScript = "INSERT INTO BUILDINGS (ID, USER, BLOCK, POSTALCODE, STREET, LEVEL, UNIT) VALUES("
    for id in range(dataSize):
        scr = prefixOfScript+str(id)+', \''+str(user)+'\', '
        for column in columns:
            if((column == "Block") or (column == "Street")):
                scr += ("\'"+list(df[column])[id]+"\'")
            else:
                scr += list(df[column])[id]
            if (column == "Unit"):
                scr += ");"
            else:
                scr += ", "
        print("Inserted "+str(id))
        c.execute(scr)
    coon.commit()
    print("Commited")
    coon.close()
    print("Closed")

def simpleSearching(field,value,filename = "database.db"):
    """this function search for objects with a certain value (int) or contains certain substring (str)
    TODO: more searching condition, output ways, robustness"""
    coon = sqlite3.connect(filename)
    print("Connected")
    c = coon.cursor()
    if((field == "BLOCK") or (field == "STREET") or (field == "USER")):
        scr = "SELECT * FROM BUILDINGS WHERE "+ field +" LIKE \'%"+ value +"%\';"
    else:
        scr = "SELECT * FROM BUILDINGS WHERE "+ field +" = "+ str(value) +";"
    c.execute(scr)
    for row in c:
        print(row)
    coon.close()
    print("Closed")

def intRangeSearching(field,value1 = "inf",value2 = "inf",filename = "database.db"):
    """this function search for objects with value (int) lying in certain range
    TODO: more searching condition, output ways, robustness"""
    coon = sqlite3.connect(filename)
    print("Connected")
    c = coon.cursor()
    if ((value1 == "inf") and (value2 == "inf")):
        scr = "SELECT * FROM BUILDINGS WHERE "+ field +" > 0;"
    if ((value1 != "inf") and (value2 == "inf")):
        scr = "SELECT * FROM BUILDINGS WHERE "+ field +" >= "+ str(value1) +";"
    if ((value1 == "inf") and (value2 != "inf")):
        scr = "SELECT * FROM BUILDINGS WHERE "+ field +" <= "+ str(value2) +";"
    if ((value1 != "inf") and (value2 != "inf")):
        scr = "SELECT * FROM BUILDINGS WHERE "+ field +" BETWEEN "+ str(value1)+" AND "+ str(value2)+";"
    c.execute(scr)
    for row in c:
        print(row)
    coon.close()
    print("Closed")