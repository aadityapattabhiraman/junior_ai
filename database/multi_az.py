#!/usr/bin/env python3

import os
from azure.storage.blob import BlobServiceClient, BlobClient
import time

# Replace with your storage connection string
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string, )#max_block_size=100*1024, max_single_put_size=100*1024, max_connections=100)

# Container and blob names
container_name = "trial"
blob_name = "trial.mp4"
local_file_path = "/home/akugyo/result (4).mp4"

def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str, blob_name, local_file_path="outpt.txt"):
    container_client = blob_service_client.get_container_client(container=container_name)
    with open(file=local_file_path, mode="rb") as data:
        blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)



if __name__ == "__main__":
    start_time = time.time()
    upload_blob_file(blob_service_client, container_name, blob_name, local_file_path)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
