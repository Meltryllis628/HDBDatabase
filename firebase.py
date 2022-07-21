from time import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import json
from osgeo import ogr
import pandas as pd
#from google.cloud import storage

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "hdbdatabase",
})
firebase_admin.initialize_app(cred, {
    'storageBucket': 'hdbdatabase.appspot.com'
})
bucket = storage.bucket()

db = firestore.client()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    #storage_client = storage.Client()
    #bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


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


