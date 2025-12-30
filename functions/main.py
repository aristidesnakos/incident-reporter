"""
Digital Foreman Cloud Functions
Handles voice-to-voice incident reporting via Telegram and ElevenLabs Conversational AI
"""

import os
import json
import logging
import base64
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import requests
from google.cloud import firestore, storage, secretmanager
import functions_framework
from flask import Request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
firestore_client = firestore.Client()
storage_client = storage.Client()
secret_client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_name: str) -> str:
    """Retrieve secret from Google Secret Manager"""
    project_id = os.environ.get("PROJECT_ID")
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

@functions_framework.http
def telegram_handler(request: Request) -> tuple[str, int]:
    """
    Handle incoming Telegram webhook requests
    Processes voice messages through ElevenLabs Conversational AI Agent
    """
    try:
        # Parse Telegram webhook payload
        update = request.get_json()
        if not update or "message" not in update:
            return "No message found", 400

        message = update["message"]
        chat_id = message["chat"]["id"]
        user_name = message.get("from", {}).get("first_name", "Unknown")
        
        # Check if message contains voice
        if "voice" not in message:
            # Send text response for non-voice messages
            send_telegram_message(chat_id, 
                "Hi! I'm Rachel from Digital Foreman safety. Please send me a voice message to report any safety incidents.")
            return "Non-voice message handled", 200

        # Download voice file from Telegram
        voice_file_id = message["voice"]["file_id"]
        voice_file_path = download_telegram_voice(voice_file_id)
        
        if not voice_file_path:
            send_telegram_message(chat_id, 
                "Sorry, I couldn't process your voice message. Please try again.")
            return "Voice download failed", 500

        # Process voice through ElevenLabs Conversational AI Agent
        response_data = process_voice_with_agent(voice_file_path, chat_id, user_name)
        
        if not response_data:
            send_telegram_message(chat_id, 
                "Sorry, there was a technical issue. Please try reporting your incident again.")
            return "Agent processing failed", 500

        # Store incident in Firestore
        incident_id = store_incident(response_data, chat_id, user_name)
        
        # Handle urgency-based routing
        handle_incident_routing(response_data, incident_id)
        
        # Send voice response back to Telegram
        if response_data.get("voice_response_url"):
            send_voice_message(chat_id, response_data["voice_response_url"])
        
        # Cleanup temp files
        cleanup_temp_file(voice_file_path)
        
        return "Voice message processed successfully", 200
        
    except Exception as e:
        logger.error(f"Error in telegram_handler: {e}")
        return f"Internal error: {str(e)}", 500

def download_telegram_voice(file_id: str) -> Optional[str]:
    """Download voice file from Telegram servers"""
    try:
        token = get_secret("telegram-bot-token")
        
        # Get file info from Telegram API
        file_info_url = f"https://api.telegram.org/bot{token}/getFile"
        response = requests.get(file_info_url, params={"file_id": file_id})
        
        if response.status_code != 200:
            logger.error(f"Failed to get file info: {response.text}")
            return None
            
        file_path = response.json()["result"]["file_path"]
        
        # Download the actual file
        file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
        file_response = requests.get(file_url)
        
        if file_response.status_code != 200:
            logger.error(f"Failed to download file: {file_response.text}")
            return None
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ogg")
        temp_file.write(file_response.content)
        temp_file.close()
        
        return temp_file.name
        
    except Exception as e:
        logger.error(f"Error downloading voice file: {e}")
        return None

def process_voice_with_agent(voice_file_path: str, chat_id: str, user_name: str) -> Optional[Dict[str, Any]]:
    """Process voice file through ElevenLabs Conversational AI Agent"""
    try:
        api_key = get_secret("elevenlabs-api-key")
        agent_id = get_secret("elevenlabs-agent-id")
        
        # Read voice file
        with open(voice_file_path, "rb") as f:
            voice_data = f.read()
        
        # Create conversation session with ElevenLabs agent
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Start conversation session
        session_response = requests.post(
            f"https://api.elevenlabs.io/v1/convai/conversations",
            headers=headers,
            json={
                "agent_id": agent_id,
                "session_id": f"telegram_{chat_id}_{datetime.now().timestamp()}"
            }
        )
        
        if session_response.status_code != 200:
            logger.error(f"Failed to create conversation session: {session_response.text}")
            return None
        
        conversation_id = session_response.json()["conversation_id"]
        
        # Send voice message to agent
        files = {"audio": ("voice.ogg", voice_data, "audio/ogg")}
        voice_response = requests.post(
            f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/messages",
            headers={"Authorization": f"Bearer {api_key}"},
            files=files
        )
        
        if voice_response.status_code != 200:
            logger.error(f"Failed to send voice to agent: {voice_response.text}")
            return None
        
        response_data = voice_response.json()
        
        # Extract structured incident data from agent response
        incident_data = extract_incident_data(response_data)
        
        # Store voice response for playback
        voice_url = None
        if response_data.get("audio_response"):
            voice_url = store_voice_response(response_data["audio_response"], chat_id)
        
        return {
            "conversation_id": conversation_id,
            "incident_data": incident_data,
            "agent_response": response_data.get("text_response", ""),
            "voice_response_url": voice_url,
            "raw_response": response_data
        }
        
    except Exception as e:
        logger.error(f"Error processing voice with agent: {e}")
        return None

def extract_incident_data(agent_response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract structured incident data from agent response"""
    try:
        # Look for JSON data in the agent's response
        response_text = agent_response.get("text_response", "")
        
        # Try to find JSON block in response
        import re
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        
        if json_match:
            json_str = json_match.group()
            incident_data = json.loads(json_str)
        else:
            # Default classification if no structured data found
            incident_data = {
                "urgency": "routine",
                "type": "general",
                "location": "unknown",
                "description": response_text,
                "confidence": 0.5,
                "requires_followup": True
            }
        
        return incident_data
        
    except Exception as e:
        logger.error(f"Error extracting incident data: {e}")
        return {
            "urgency": "routine",
            "type": "general", 
            "location": "unknown",
            "description": "Voice message received",
            "confidence": 0.1,
            "requires_followup": True
        }

def store_voice_response(audio_data: bytes, chat_id: str) -> str:
    """Store voice response in Cloud Storage and return URL"""
    try:
        bucket_name = os.environ.get("AUDIO_BUCKET")
        bucket = storage_client.bucket(bucket_name)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"responses/{chat_id}_{timestamp}_response.mp3"
        
        blob = bucket.blob(blob_name)
        blob.upload_from_string(audio_data, content_type="audio/mpeg")
        
        return f"gs://{bucket_name}/{blob_name}"
        
    except Exception as e:
        logger.error(f"Error storing voice response: {e}")
        return None

def store_incident(response_data: Dict[str, Any], chat_id: str, user_name: str) -> str:
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
        doc_ref = firestore_client.collection("incidents").document()
        doc_ref.set(incident_doc)
        
        logger.info(f"Stored incident {doc_ref.id} with urgency: {incident_data.get('urgency')}")
        return doc_ref.id
        
    except Exception as e:
        logger.error(f"Error storing incident: {e}")
        return None

def handle_incident_routing(response_data: Dict[str, Any], incident_id: str):
    """Route incident based on urgency level"""
    try:
        urgency = response_data["incident_data"].get("urgency", "routine").lower()
        
        if urgency == "emergency":
            # Send emergency email alert
            send_emergency_email(response_data, incident_id)
        elif urgency == "urgent":
            # Send urgent notification (could be Telegram alert to managers)
            logger.info(f"Urgent incident {incident_id} - notification system would trigger")
        
        # Routine incidents just get logged
        logger.info(f"Incident {incident_id} routed with urgency: {urgency}")
        
    except Exception as e:
        logger.error(f"Error routing incident: {e}")

def send_emergency_email(response_data: Dict[str, Any], incident_id: str):
    """Send emergency email alert via Gmail API"""
    try:
        # This would integrate with Gmail API
        # For now, just log the emergency
        incident = response_data["incident_data"]
        logger.warning(f"EMERGENCY INCIDENT {incident_id}: {incident.get('description', 'No description')}")
        logger.warning(f"Location: {incident.get('location', 'Unknown')}")
        
        # In production, implement Gmail API integration here
        
    except Exception as e:
        logger.error(f"Error sending emergency email: {e}")

def send_telegram_message(chat_id: str, text: str):
    """Send text message via Telegram Bot API"""
    try:
        token = get_secret("telegram-bot-token")
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        requests.post(url, json={
            "chat_id": chat_id,
            "text": text
        })
        
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")

def send_voice_message(chat_id: str, voice_url: str):
    """Send voice message via Telegram Bot API"""
    try:
        if not voice_url or not voice_url.startswith("gs://"):
            return
        
        # Download voice from Cloud Storage
        bucket_name = voice_url.split("/")[2]
        blob_name = "/".join(voice_url.split("/")[3:])
        
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        voice_data = blob.download_as_bytes()
        
        # Send via Telegram
        token = get_secret("telegram-bot-token")
        url = f"https://api.telegram.org/bot{token}/sendVoice"
        
        files = {"voice": ("response.mp3", voice_data, "audio/mpeg")}
        data = {"chat_id": chat_id}
        
        requests.post(url, files=files, data=data)
        
    except Exception as e:
        logger.error(f"Error sending voice message: {e}")

def cleanup_temp_file(file_path: str):
    """Clean up temporary files"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up temp file: {e}")

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

@functions_framework.http  
def followup_scheduler(request: Request) -> tuple[str, int]:
    """Scheduled function to send follow-up messages for unresolved incidents"""
    try:
        # Query open incidents older than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        incidents = firestore_client.collection("incidents").where(
            "status", "==", "open"
        ).where(
            "created_at", "<", cutoff_time.isoformat()
        ).limit(50).stream()
        
        followup_count = 0
        
        for incident_doc in incidents:
            incident_data = incident_doc.to_dict()
            incident_id = incident_doc.id
            
            # Send follow-up voice message
            success = send_followup_message(incident_data, incident_id)
            
            if success:
                # Update follow-up count
                incident_doc.reference.update({
                    "follow_ups": firestore.ArrayUnion([{
                        "timestamp": datetime.utcnow().isoformat(),
                        "type": "24h_followup",
                        "sent": True
                    }])
                })
                followup_count += 1
        
        logger.info(f"Sent {followup_count} follow-up messages")
        return f"Sent {followup_count} follow-ups", 200
        
    except Exception as e:
        logger.error(f"Error in followup_scheduler: {e}")
        return f"Follow-up error: {str(e)}", 500

def send_followup_message(incident_data: Dict[str, Any], incident_id: str) -> bool:
    """Send follow-up message for an unresolved incident"""
    try:
        user_id = incident_data.get("user_id")
        if not user_id:
            return False
        
        # Create follow-up message
        description = incident_data.get("classification", {}).get("description", "your safety report")
        message = f"Hi! This is Rachel following up on {description}. Has this safety issue been resolved?"
        
        send_telegram_message(user_id, message)
        return True
        
    except Exception as e:
        logger.error(f"Error sending follow-up: {e}")
        return False