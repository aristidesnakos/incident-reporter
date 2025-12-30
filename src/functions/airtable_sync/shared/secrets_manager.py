"""
Google Secret Manager utilities
"""

import os
import logging
from google.cloud import secretmanager

logger = logging.getLogger(__name__)

# Global client instance
secret_client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_name: str) -> str:
    """Retrieve secret from Google Secret Manager"""
    try:
        project_id = os.environ.get("PROJECT_ID")
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
        return ""