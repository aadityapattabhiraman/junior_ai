#!/usr/bin/env python3

from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings
import os

# Replace with your actual connection string and blob details
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = 'trial'
blob_name = 'output.txt'
file_path = '/home/akugyo/GitHub/intern/FDP/output.txt'  # Path to the file you want to upload

# Create a BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a BlobClient object
blob_client = blob_service_client.get_blob_client(container_name, blob_name)

# Set chunk size in bytes
chunk_size = 1024 * 1024  # 4MB, maximum size for each chunk is 4MB

# Open the file to be uploaded
with open(file_path, "rb") as data:
    try:
        # Create a list to keep track of block IDs
        block_list = []

        index = 0
        while True:
            # Read a chunk of data
            chunk = data.read(chunk_size)
            if not chunk:
                break

            # Generate a block ID (block IDs must be base64 encoded)
            block_id = f"{index:08d}"
            block_id_encoded = block_id.encode('utf-8')

            # Upload the chunk as a block to Azure Blob Storage
            blob_client.stage_block(block_id, chunk)
            block_list.append(BlobBlock(block_id=block_id_encoded))

            index += 1
            print(f"Uploaded chunk {index}")

        # Commit the list of blocks to the blob
        blob_client.commit_block_list(block_list)

        print(f"Upload completed for blob '{blob_name}'")
    except Exception as e:
        print(f"Error uploading blob: {e}")
