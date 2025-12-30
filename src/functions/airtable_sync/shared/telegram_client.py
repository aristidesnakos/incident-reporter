"""
Telegram Bot API client utilities
"""

import os
import logging
import tempfile
import requests
from typing import Optional
from .secrets_manager import get_secret
from .storage_client import StorageClient

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self):
        self.storage_client = StorageClient()
    
    def send_message(self, chat_id: str, text: str):
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
    
    def send_voice_message(self, chat_id: str, voice_url: str):
        """Send voice message via Telegram Bot API"""
        try:
            if not voice_url or not voice_url.startswith("gs://"):
                return
            
            # Download voice from Cloud Storage
            voice_data = self.storage_client.download_file(voice_url)
            if not voice_data:
                return
            
            # Send via Telegram
            token = get_secret("telegram-bot-token")
            url = f"https://api.telegram.org/bot{token}/sendVoice"
            
            files = {"voice": ("response.mp3", voice_data, "audio/mpeg")}
            data = {"chat_id": chat_id}
            
            requests.post(url, files=files, data=data)
            
        except Exception as e:
            logger.error(f"Error sending voice message: {e}")
    
    def download_voice_file(self, file_id: str) -> Optional[str]:
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