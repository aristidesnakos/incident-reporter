"""
Firestore client utilities for Digital Foreman
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from google.cloud import firestore

logger = logging.getLogger(__name__)

class FirestoreClient:
    def __init__(self):
        self.client = firestore.Client()
    
    def store_incident(self, response_data: Dict[str, Any], chat_id: str, user_name: str) -> str:
        """Store incident data in Firestore"""
        try:
            incident_data = response_data["incident_data"]
            
            incident_doc = {
                "timestamp": firestore.SERVER_TIMESTAMP,
                "user_id": str(chat_id),
                "user_name": user_name,
                "conversation": {
                    "conversation_id": response_data.get("conversation_id"),
                    "agent_response": response_data.get("agent_response", ""),
                    "voice_response_url": response_data.get("voice_response_url")
                },
                "classification": {
                    "urgency": incident_data.get("urgency", "routine"),
                    "type": incident_data.get("type", "general"),
                    "location": incident_data.get("location", "unknown"),
                    "description": incident_data.get("description", ""),
                    "confidence": incident_data.get("confidence", 0.5)
                },
                "status": "open",
                "requires_followup": incident_data.get("requires_followup", True),
                "follow_ups": [],
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Add to Firestore
            doc_ref = self.client.collection("incidents").document()
            doc_ref.set(incident_doc)
            
            logger.info(f"Stored incident {doc_ref.id} with urgency: {incident_data.get('urgency')}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Error storing incident: {e}")
            return None
    
    def get_open_incidents(self, hours_old: int = 24, limit: int = 50):
        """Get open incidents older than specified hours"""
        from datetime import timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_old)
        
        return self.client.collection("incidents").where(
            "status", "==", "open"
        ).where(
            "created_at", "<", cutoff_time.isoformat()
        ).limit(limit).stream()
    
    def add_followup(self, incident_id: str, followup_data: Dict[str, Any]):
        """Add follow-up to existing incident"""
        try:
            doc_ref = self.client.collection("incidents").document(incident_id)
            doc_ref.update({
                "follow_ups": firestore.ArrayUnion([followup_data])
            })
            return True
        except Exception as e:
            logger.error(f"Error adding follow-up: {e}")
            return False