class Upload(APIView):
     
    def post(self, request):
        storage_account_key = ""
        storage_account_name = ""
        connection_string = ""
        container_name = ""
        file = request.FILES["file_name"]
        filename = file.name
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
        #blob_item= blob_service_client.get_blob_to_bytes(container_name, filename)
        if blob_client.exists():
            blob_client.delete_blob()
        #with open(request.FILES.get('file_name'), 'rb') as data:
        blob_client.upload_blob(file.read())
        return HttpResponse("File Uploaded Sucessfully")

class LoadChart(APIView):
    def get(self, request):
        filename = request.query_params['projectName']
        storage_account_key = ""
        storage_account_name = ""
        connection_string = ""
        container_name = ""
        sas = generate_blob_sas(
          account_name = storage_account_name,
          container_name = container_name,
          blob_name = filename,
          account_key = storage_account_key,
          permission = BlobSasPermissions(read=True),
          expiry = datetime.utcnow() + timedelta(hours = 1)
        )
        blob_url = f'https://{storage_account_name}.blob.core.windows.net/{container_name}/{filename}?{sas}'
        df = pd.read_excel(blob_url)
        print(df)
        return HttpResponse("File fetched Sucessfully")

from azure.storage.blob import BlobServiceClient
import pandas as pd

STORAGEACCOUNTURL= ""
STORAGEACCOUNTKEY= ""
LOCALFILENAME= ""
CONTAINERNAME= ""
BLOBNAME= ""

#download from blob
t1=time.time()
blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, BLOBNAME, snapshot=None)
with open(LOCALFILENAME, "wb") as my_blob:
    blob_data = blob_client_instance.download_blob()
    blob_data.readinto(my_blob)
t2=time.time()
print(("It takes %s seconds to download "+BLOBNAME) % (t2 - t1))
