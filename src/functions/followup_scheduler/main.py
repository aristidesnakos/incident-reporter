"""
Follow-up Scheduler Cloud Function
Sends automated follow-up messages for unresolved incidents
"""

import logging
from datetime import datetime
import functions_framework
from flask import Request

from shared.firestore_client import FirestoreClient
from shared.telegram_client import TelegramClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
firestore_client = FirestoreClient()
telegram_client = TelegramClient()

def send_followup_message(incident_data: dict, incident_id: str) -> bool:
    """Send follow-up message for an unresolved incident"""
    try:
        user_id = incident_data.get("user_id")
        if not user_id:
            return False
        
        # Create follow-up message
        description = incident_data.get("classification", {}).get("description", "your safety report")
        message = f"Hi! This is Rachel following up on {description}. Has this safety issue been resolved?"
        
        telegram_client.send_message(user_id, message)
        return True
        
    except Exception as e:
        logger.error(f"Error sending follow-up: {e}")
        return False

@functions_framework.http  
def followup_scheduler(request: Request) -> tuple[str, int]:
    """Scheduled function to send follow-up messages for unresolved incidents"""
    try:
        # Query open incidents older than 24 hours
        incidents = firestore_client.get_open_incidents(hours_old=24, limit=50)
        
        followup_count = 0
        
        for incident_doc in incidents:
            incident_data = incident_doc.to_dict()
            incident_id = incident_doc.id
            
            # Send follow-up voice message
            success = send_followup_message(incident_data, incident_id)
            
            if success:
                # Update follow-up count
                followup_data = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "24h_followup",
                    "sent": True
                }
                
                firestore_client.add_followup(incident_id, followup_data)
                followup_count += 1
        
        logger.info(f"Sent {followup_count} follow-up messages")
        return f"Sent {followup_count} follow-ups", 200
        
    except Exception as e:
        logger.error(f"Error in followup_scheduler: {e}")
        return f"Follow-up error: {str(e)}", 500