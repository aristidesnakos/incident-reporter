"""
Telegram Voice Handler Cloud Function
Handles voice messages via ElevenLabs Conversational AI Agent
"""

import os
import logging
import functions_framework
from flask import Request

from shared.telegram_client import TelegramClient
from shared.elevenlabs_client import ElevenLabsClient
from shared.firestore_client import FirestoreClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
telegram_client = TelegramClient()
elevenlabs_client = ElevenLabsClient()
firestore_client = FirestoreClient()

def cleanup_temp_file(file_path: str):
    """Clean up temporary files"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up temp file: {e}")

def handle_incident_routing(response_data: dict, incident_id: str):
    """Route incident based on urgency level - simplified without email"""
    try:
        urgency = response_data["incident_data"].get("urgency", "routine").lower()
        
        if urgency == "emergency":
            logger.warning(f"EMERGENCY INCIDENT {incident_id}: {response_data['incident_data'].get('description', 'No description')}")
            logger.warning(f"Location: {response_data['incident_data'].get('location', 'Unknown')}")
        elif urgency == "urgent":
            logger.info(f"Urgent incident {incident_id} - monitoring required")
        
        # All incidents get logged, but no email alerts
        logger.info(f"Incident {incident_id} routed with urgency: {urgency}")
        
    except Exception as e:
        logger.error(f"Error routing incident: {e}")

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
            telegram_client.send_message(chat_id, 
                "Hi! I'm Rachel from Digital Foreman safety. Please send me a voice message to report any safety incidents.")
            return "Non-voice message handled", 200

        # Download voice file from Telegram
        voice_file_id = message["voice"]["file_id"]
        voice_file_path = telegram_client.download_voice_file(voice_file_id)
        
        if not voice_file_path:
            telegram_client.send_message(chat_id, 
                "Sorry, I couldn't process your voice message. Please try again.")
            return "Voice download failed", 500

        # Process voice through ElevenLabs Conversational AI Agent
        response_data = elevenlabs_client.process_voice_with_agent(voice_file_path, chat_id, user_name)
        
        if not response_data:
            telegram_client.send_message(chat_id, 
                "Sorry, there was a technical issue. Please try reporting your incident again.")
            return "Agent processing failed", 500

        # Store incident in Firestore
        incident_id = firestore_client.store_incident(response_data, chat_id, user_name)
        
        # Handle urgency-based routing (no email alerts)
        handle_incident_routing(response_data, incident_id)
        
        # Send voice response back to Telegram
        if response_data.get("voice_response_url"):
            telegram_client.send_voice_message(chat_id, response_data["voice_response_url"])
        
        # Cleanup temp files
        cleanup_temp_file(voice_file_path)
        
        return "Voice message processed successfully", 200
        
    except Exception as e:
        logger.error(f"Error in telegram_handler: {e}")
        return f"Internal error: {str(e)}", 500