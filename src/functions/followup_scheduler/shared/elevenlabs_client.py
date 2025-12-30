"""
ElevenLabs Conversational AI client utilities
"""

import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from .secrets_manager import get_secret
from .storage_client import StorageClient

logger = logging.getLogger(__name__)

class ElevenLabsClient:
    def __init__(self):
        self.storage_client = StorageClient()
    
    def process_voice_with_agent(self, voice_file_path: str, chat_id: str, user_name: str) -> Optional[Dict[str, Any]]:
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
            incident_data = self.extract_incident_data(response_data)
            
            # Store voice response for playback
            voice_url = None
            if response_data.get("audio_response"):
                voice_url = self.storage_client.store_voice_response(response_data["audio_response"], chat_id)
            
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
    
    def extract_incident_data(self, agent_response: Dict[str, Any]) -> Dict[str, Any]:
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