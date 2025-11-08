from pocketbase import PocketBase  # Client also works the same
from pocketbase.client import FileUpload
import os, shutil, time
from dotenv import load_dotenv

load_dotenv()


client = PocketBase('https://anas099.duckdns.org')

access_token = os.getenv("PBTOKEN")

def upload_media(file_path:str):

 # create record and upload file to image field
 result = client.collection("temp_storage").create(
    {
        "file": FileUpload((file_path, open(file_path, "rb"))),
    },{"pbtoken": access_token})


 record = client.collection("temp_storage").get_one(result.id)

 return client.get_file_url(record,record.file)  # get file url

#upload_media("uploads/sample.txt")  # example usage
 
