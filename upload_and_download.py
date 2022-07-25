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

def upload_blob(source_file_path, destination_blob_name):
    """Uploads a file to the bucket."""
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
        f"Downloaded storage object {source_blob_name} from bucket to local file {destination_file_name}."
    )

def upload_all_files(gdb_file_path,xls_file_path,output_file_path,uuid):
    #TODO: add files separately
    doc_ref = db.collection(u'records').document(uuid)
    doc_ref.set({u'uploadTime':firestore.SERVER_TIMESTAMP,
                u'uuid':uuid})
    print(f"File info uploaded to database.")
    gdb_blob = uuid + r"/gdb" 
    doc_ref.update({u"input1_url":gdb_blob})
    xls_blob = uuid + r"/xls"
    doc_ref.update({u"input2_url":xls_blob})
    output_blob = uuid + r"/output"
    doc_ref.update({u"output_url":output_blob})
    upload_blob(gdb_file_path,gdb_blob)
    upload_blob(xls_file_path,xls_blob)
    upload_blob(output_file_path,output_blob)

def download_all_files(gdb_file_path,xls_file_path,output_file_path,uuid):
    #TODO: finish it
    doc_ref = db.collection(u'records').document(uuid)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')

def file_list():
    jsonString = "["
    records = db.collection(u'records').stream()
    for record in records:
        recordDict = record.to_dict()
        try:
            recordDict["uploadTime"] = str(recordDict["uploadTime"])
        except:
            pass
        try:
            recordDict["create_time"] = str(recordDict["create_time"])
        except:
            pass
        recordStr = str(recordDict)
        jsonString += (recordStr + ", ")
    jsonString = jsonString[:-2]
    jsonString += "]"
    return jsonString#a string


def delete_certain_file(uuid):
    try:
        db.collection(u'records').document(uuid).delete()
        print("Deleted")
    except:
        print("Delete Failed")
json = file_list()
#print(json)
# uuid = "test0"
# gdb_file_path = "test.gdb"
# xls_file_path = "test.xls"
# output_file_path = "testout.xls"
# upload_all_files(gdb_file_path,xls_file_path,output_file_path,uuid)

