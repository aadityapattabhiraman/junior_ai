#!/usr/bin/env python3

from azure.mgmt.media import AzureMediaServicesClient
from azure.common.credentials import ServicePrincipalCredentials

# Replace with your details
subscription_id = "<your_subscription_id>"
resource_group_name = "<your_resource_group_name>"
account_name = "<your_ams_account_name>"
client_secret = "<your_client_secret>"
client_id = "<your_client_id>"
tenant = "<your_tenant_id>"

# Upload your video file to Azure Storage (e.g., Blob Storage) before proceeding
# Get the uploaded video's details (container name, blob name)

# Create credentials
credentials = ServicePrincipalCredentials(
    client_id=client_id, secret=client_secret, tenant=tenant
)

# Create AMS client
client = AzureMediaServicesClient(credentials, subscription_id)

# Create an Asset
asset_name = "my-video-asset"
create_asset_response = client.assets.create(
    resource_group_name, account_name, asset_name, {"storage_account": "<your_storage_account_name>"}
)

# Wait for asset creation to complete (optional)
create_asset_response.wait()

# Get the uploaded video details (replace with actual container and blob names)
container_name = "<your_container_name>"
blob_name = "<your_blob_name.mp4>"  # Ensure file extension is included

# Update the Asset with the uploaded video (Specify container and blob)
update_asset_response = client.assets.update(
    resource_group_name, account_name, asset_name, {"uri": f"azure-storage://{container_name}/{blob_name}"}
)

# Wait for asset update to complete (optional)
update_asset_response.wait()

# Generate a streaming URL (replace with desired format)
list_streaming_endpoints_response = client.streaming_endpoints.list(resource_group_name, account_name)
streaming_endpoint = list_streaming_endpoints_response.value[0]  # Assuming you have a single endpoint

# Get a streaming locator for playback (replace with desired format)
streaming_locator_name = "my-streaming-locator"
create_locator_response = client.streaming_locators.create(
    resource_group_name, account_name, streaming_endpoint.name, streaming_locator_name, {"asset_name": asset_name, "content_keys": []}
)

# Wait for locator creation to complete (optional)
create_locator_response.wait()

# Access the streaming URL from the locator
streaming_url = create_locator_response.content_delivery_urls["default"] + "/manifest"

print(f"Streaming URL: {streaming_url}")
