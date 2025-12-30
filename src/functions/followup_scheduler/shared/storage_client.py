"""
Google Cloud Storage client utilities
"""

import os
import logging
from datetime import datetime
from google.cloud import storage

logger = logging.getLogger(__name__)

class StorageClient:
    def __init__(self):
        self.client = storage.Client()
    
    def store_voice_response(self, audio_data: bytes, chat_id: str) -> str:
        """Store voice response in Cloud Storage and return URL"""
        try:
            bucket_name = os.environ.get("AUDIO_BUCKET")
            bucket = self.client.bucket(bucket_name)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            blob_name = f"responses/{chat_id}_{timestamp}_response.mp3"
            
            blob = bucket.blob(blob_name)
            blob.upload_from_string(audio_data, content_type="audio/mpeg")
            
            return f"gs://{bucket_name}/{blob_name}"
            
        except Exception as e:
            logger.error(f"Error storing voice response: {e}")
            return None
    
    def download_file(self, gs_url: str) -> bytes:
        """Download file from Cloud Storage"""
        try:
            # Parse gs:// URL
            bucket_name = gs_url.split("/")[2]
            blob_name = "/".join(gs_url.split("/")[3:])
            
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            return blob.download_as_bytes()
            
        except Exception as e:
            logger.error(f"Error downloading file from {gs_url}: {e}")
            return None