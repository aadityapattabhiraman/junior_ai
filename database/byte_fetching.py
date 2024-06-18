#!/usr/bin/env python3

from azure.storage.blob import BlobServiceClient


connection_string = 'your_connection_string'
container_name = 'your_container_name'
blob_name = 'your_blob_name'
output_file_path = 'output_file.txt'

start_range = 0
end_range = 99

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

blob_client = blob_service_client.get_blob_client(container_name, blob_name)

try:
    with open(output_file_path, "wb") as my_blob:
        blob_data = blob_client.download_blob(range=(start_range, end_range))
        my_blob.write(blob_data.readall())
    print(f"Byte range {start_range}-{end_range} of blob '{blob_name}' downloaded to '{output_file_path}'")
except Exception as e:
    print(f"Error downloading blob range: {e}")
