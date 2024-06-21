#!/usr/bin/env python3

import os
from azure.storage.blob import BlobServiceClient, BlobClient

oconnection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string, max_block_size=1024*1024, max_single_put_size=2*1024*1024)
cntainer_name = "trial"
blob_name = "mp.mp4"

def download_blob_chunks(blob_service_client: BlobServiceClient, container_name, blob_name, local_file_path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # This returns a StorageStreamDownloader
    stream = blob_client.download_blob()
    chunk_list = []

    with open(local_file_path, "wb") as f:
    # Read data in chunks to avoid loading all into memory at once
        for chunk in stream.chunks():
        # Process your data (anything can be done here - 'chunk' is a byte array)
            chunk_list.append(chunk)
            f.write(chunk)


if __name__ == "__main__":
    download_blob_chunks(blob_service_client, container_name, blob_name, local_file_path="mp.mp4")
