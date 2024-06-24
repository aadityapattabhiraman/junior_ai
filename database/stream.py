#!/usr/bin/env python3

import os
from azure.storage.blob import BlobServiceClient, ContentSettings
import time

# this function uploads a file to Azure Blob Storage and also streams it back
def upload_and_stream(local_file_path: str):

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    endpoint = "https://endpoint-dhe0dcf3akg0e4ec.a01.azurefd.net/"
    container_name = "hitman"

    blob_name = local_file_path.split("/")
    blob_name = blob_name[-1]
    blob_name = blob_name.lower().replace(" ", "_")
    container_client = blob_service_client.get_container_client(container=container_name)
    content_settings = ContentSettings(content_type='video/mp4')

    with open(file=local_file_path, mode="rb") as data:

        container_client.upload_blob(name=blob_name, data=data, overwrite=True, 
            content_settings=content_settings)

    
    return endpoint + container_name + "/" + blob_name


if __name__ == '__main__':
    start = time.time()
    print(upload_and_stream("/home/akugyo/result.mp4"))
    stop = time.time()
    print(stop-start)