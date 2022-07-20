import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import json
from osgeo import ogr
import pandas as pd
import time
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "hdbdatabase",
  'storageBucket': 'hdbdatabase.appspot.com'
})

bucket = storage.bucket()
db = firestore.client()

def generating_file_id(user_id):
    """Generate file id by its uploading time and user's id."""
    return user_id+str(int(time.time()*10000000))

# def get_data_from_json_file(source_file_path):
#     """This Function takes json file as input and returns a Dataframe"""
#     file = open(source_file_path,'rb')
#     try:
#         content = file.read() 
#         features = json.loads(content)
#         df = pd.DataFrame(features)
#         return(df)
#     finally:
#         file.close()

def upload_blob(source_file_path, destination_blob_name):
    """Uploads a file to the bucket."""
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(
        f"File {source_file_path} uploaded to {destination_blob_name}."
    )

def download_blob(source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket to local file {}.".format(
            source_blob_name, destination_file_name
        )
    )

def adding_data(file_name,file_id,user_id):
    """This Function adds data into database from Dataframe"""
    doc_ref = db.collection(u'files').document(file_name)
    # dataSize = df.shape[0]
    # columns = ['Block', 'PostalCode', 'Street', 'Level', 'Unit']
    doc_ref.set({u'uploadTime':firestore.SERVER_TIMESTAMP,
                  u'fileName':file_name,
                  u'fileId':file_id,
                  u'userId':user_id})
    print(
        f"File {file_name} uploaded to database."
    )
    # for i in range(dataSize):
    #     row_ref = doc_ref.collection(u'records').document(str(i))
    #     row_ref.set({"id":i})
    #     for column in columns:
    #         row_ref.update({column:list(df[column])[i]})

def upload_ultimate(file_name,source_file_path,user_id):
    file_id = generating_file_id(user_id) # or something else, need to be unique for every file
    adding_data(file_name,file_id,user_id)
    upload_blob(source_file_path,file_id)

def download_ultimate(file_name,destination_file_name,user_id):
    # Create a reference to the cities collection
    files_ref = db.collection(u'files')
    # Create a query against the collection
    query_ref = files_ref.where(u'fileName', u'==', u'file_name')

bolb = "0966db90-06b1-11ed-afe2-acde48001122/gdb"
destination_file_name = "download.gdb"
download_blob(bolb, destination_file_name)
#upload_ultimate_json("test.json","test.json","0022")