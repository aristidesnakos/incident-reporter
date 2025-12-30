"""
Airtable Sync Cloud Function
Syncs incident data from Firestore to Airtable dashboard
"""

import logging
import requests
from datetime import datetime
import functions_framework

from shared.secrets_manager import get_secret

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.cloud_event
def airtable_sync(cloud_event):
    """Sync new incident data to Airtable"""
    try:
        # Extract incident data from Firestore change event
        incident_data = cloud_event.data.get("value", {}).get("fields", {})
        incident_id = cloud_event.data.get("value", {}).get("name", "").split("/")[-1]
        
        if not incident_data:
            logger.info("No incident data in event")
            return
        
        # Prepare Airtable record
        airtable_record = {
            "fields": {
                "Incident ID": incident_id,
                "Timestamp": incident_data.get("created_at", datetime.utcnow().isoformat()),
                "User Name": incident_data.get("user_name", "Unknown"),
                "Urgency": incident_data.get("classification", {}).get("urgency", "routine").title(),
                "Type": incident_data.get("classification", {}).get("type", "general").title(),
                "Location": incident_data.get("classification", {}).get("location", "Unknown"),
                "Description": incident_data.get("classification", {}).get("description", ""),
                "Status": incident_data.get("status", "open").title(),
                "Confidence": incident_data.get("classification", {}).get("confidence", 0.0)
            }
        }
        
        # Send to Airtable
        api_key = get_secret("airtable-api-key")
        base_id = get_secret("airtable-base-id")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"https://api.airtable.com/v0/{base_id}/Incidents",
            headers=headers,
            json=airtable_record
        )
        
        if response.status_code == 200:
            logger.info(f"Successfully synced incident {incident_id} to Airtable")
        else:
            logger.error(f"Failed to sync to Airtable: {response.text}")
            
    except Exception as e:
        logger.error(f"Error in airtable_sync: {e}")