variable "project_id" {
  description = "Google Cloud Project ID where resources will be created"
  type        = string
  validation {
    condition     = length(var.project_id) > 0
    error_message = "Project ID must not be empty."
  }
}

variable "region" {
  description = "Google Cloud Region for resources"
  type        = string
  default     = "us-central1"
  validation {
    condition = contains([
      "us-central1", "us-east1", "us-west1", "us-west2",
      "europe-west1", "europe-west2", "asia-southeast1"
    ], var.region)
    error_message = "Region must be a valid Google Cloud region."
  }
}

variable "telegram_bot_token" {
  description = "Telegram Bot Token from @BotFather"
  type        = string
  sensitive   = true
  validation {
    condition     = length(var.telegram_bot_token) > 0
    error_message = "Telegram bot token must not be empty."
  }
}

variable "elevenlabs_api_key" {
  description = "ElevenLabs API Key from elevenlabs.io dashboard"
  type        = string
  sensitive   = true
  validation {
    condition     = length(var.elevenlabs_api_key) > 0
    error_message = "ElevenLabs API key must not be empty."
  }
}

variable "elevenlabs_agent_id" {
  description = "ElevenLabs Conversational Agent ID"
  type        = string
  validation {
    condition     = length(var.elevenlabs_agent_id) > 0
    error_message = "ElevenLabs agent ID must not be empty."
  }
}


variable "airtable_api_key" {
  description = "Airtable API Key from airtable.com/api"
  type        = string
  sensitive   = true
  validation {
    condition     = length(var.airtable_api_key) > 0
    error_message = "Airtable API key must not be empty."
  }
}

variable "airtable_base_id" {
  description = "Airtable Base ID (starts with 'app')"
  type        = string
  validation {
    condition     = can(regex("^app[a-zA-Z0-9]+$", var.airtable_base_id))
    error_message = "Airtable base ID must start with 'app' followed by alphanumeric characters."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

