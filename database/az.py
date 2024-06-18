#!/usr/bin/env python3

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_client = blob_service_client.create_container("trial")
containers = blob_service_client.list_containers()

for container in containers:
    print(container.name)
