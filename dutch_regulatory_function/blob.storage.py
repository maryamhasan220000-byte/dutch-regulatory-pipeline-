import os
from datetime import datetime, timezone 
from azure.storage.blob import BlobServiceClient
from logger import get_logger

logger = get_logger(__name__)

def upload_raw_xml(source_name: str, raw_xml: str)-> None:
    connection_string = os.getenv('BLOB_CONNECTION_STRING')

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client('raw-publications')
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%S')
        blob_name = f"{source_name}/{timestamp}.xml"
        container_client.upload_blob(name=blob_name, data=raw_xml, overwrite=True)
    except Exception as e:
        logger.error(f"failed to upload raw XML backup for {source_name}: {e}")
