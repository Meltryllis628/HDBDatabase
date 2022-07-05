from time import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from osgeo import ogr
import pandas as pd

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "hdbdatabase",
})

db = firestore.client()

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

def addingData(df,filename):
    """This Function adds data into database from Dataframe"""
    doc_ref = db.collection(u'files').document(filename)
    dataSize = df.shape[0]
    columns = ['Block', 'PostalCode', 'Street', 'Level', 'Unit']
    doc_ref.set({u'uploadTime':firestore.SERVER_TIMESTAMP,
                  u'fileName':filename})
    for i in range(dataSize):
        row_ref = doc_ref.collection(u'records').document(str(i))
        row_ref.set({"id":i})
        for column in columns:
            row_ref.update({column:list(df[column])[i]})


