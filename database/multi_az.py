#!/usr/bin/env python3

import os
from azure.storage.blob import BlobServiceClient, BlobClient

# Replace with your storage connection string
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string, max_block_size=1024*1024, max_single_put_size=2*1024*1024)

# Container and blob names
container_name = "trial"
blob_name = "large_file.txt"
local_file_path = "/home/akugyo/GitHub/intern/FDP/output.txt"

def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str, blob_name, local_file_path):
    container_client = blob_service_client.get_container_client(container=container_name)
    with open(file=local_file_path, mode="rb") as data:
        blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)



if __name__ == "__main__":
    upload_blob_file(blob_service_client, container_name, blob_name, local_file_path)
