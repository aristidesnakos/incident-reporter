terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.4"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "telegram_bot_token" {
  description = "Telegram Bot Token from @BotFather"
  type        = string
  sensitive   = true
}

variable "elevenlabs_api_key" {
  description = "ElevenLabs API Key"
  type        = string
  sensitive   = true
}

variable "elevenlabs_agent_id" {
  description = "ElevenLabs Conversational Agent ID"
  type        = string
}


variable "airtable_pat" {
  description = "Airtable API Key"
  type        = string
  sensitive   = true
}

variable "airtable_base_id" {
  description = "Airtable Base ID"
  type        = string
}

# Random suffix for unique resource names
resource "random_id" "suffix" {
  byte_length = 4
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudscheduler.googleapis.com",
    "firestore.googleapis.com",
    "storage.googleapis.com",
    "secretmanager.googleapis.com",
    "eventarc.googleapis.com"
  ])
  
  project = var.project_id
  service = each.key
  
  disable_on_destroy = false
}

# Firestore database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Storage bucket for audio files and function source
resource "google_storage_bucket" "audio_files" {
  name     = "incident-reporter-audio-${random_id.suffix.hex}"
  location = var.region
  
  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
  
  uniform_bucket_level_access = true
  
  depends_on = [google_project_service.required_apis]
}

resource "google_storage_bucket" "function_source" {
  name     = "incident-reporter-functions-${random_id.suffix.hex}"
  location = var.region
  
  uniform_bucket_level_access = true
  
  depends_on = [google_project_service.required_apis]
}

# Service account for Cloud Functions
resource "google_service_account" "function_service_account" {
  account_id   = "incident-reporter-functions"
  display_name = "Incident Reporter Functions Service Account"
  description  = "Service account for incident reporter Cloud Functions"
}

# IAM roles for function service account
resource "google_project_iam_member" "function_permissions" {
  for_each = toset([
    "roles/datastore.user",
    "roles/storage.admin", 
    "roles/secretmanager.secretAccessor",
    "roles/logging.logWriter",
    "roles/cloudbuild.builds.builder"
  ])
  
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.function_service_account.email}"
}

# Secrets
resource "google_secret_manager_secret" "telegram_bot_token" {
  secret_id = "telegram-bot-token"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "telegram_bot_token" {
  secret      = google_secret_manager_secret.telegram_bot_token.id
  secret_data = var.telegram_bot_token
}

resource "google_secret_manager_secret" "elevenlabs_api_key" {
  secret_id = "elevenlabs-api-key"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "elevenlabs_api_key" {
  secret      = google_secret_manager_secret.elevenlabs_api_key.id
  secret_data = var.elevenlabs_api_key
}

resource "google_secret_manager_secret" "elevenlabs_agent_id" {
  secret_id = "elevenlabs-agent-id"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "elevenlabs_agent_id" {
  secret      = google_secret_manager_secret.elevenlabs_agent_id.id
  secret_data = var.elevenlabs_agent_id
}


resource "google_secret_manager_secret" "airtable_pat" {
  secret_id = "airtable-api-key"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "airtable_pat" {
  secret      = google_secret_manager_secret.airtable_pat.id
  secret_data = var.airtable_pat
}

resource "google_secret_manager_secret" "airtable_base_id" {
  secret_id = "airtable-base-id"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "airtable_base_id" {
  secret      = google_secret_manager_secret.airtable_base_id.id
  secret_data = var.airtable_base_id
}

# Create zip files for each Cloud Function
data "archive_file" "telegram_handler_zip" {
  type        = "zip"
  output_path = "/tmp/telegram-handler-source.zip"
  source_dir  = "../src/functions/telegram_handler"
}

data "archive_file" "airtable_sync_zip" {
  type        = "zip"
  output_path = "/tmp/airtable-sync-source.zip"
  source_dir  = "../src/functions/airtable_sync"
}

data "archive_file" "followup_scheduler_zip" {
  type        = "zip"
  output_path = "/tmp/followup-scheduler-source.zip"
  source_dir  = "../src/functions/followup_scheduler"
}

# Upload function sources to Cloud Storage
resource "google_storage_bucket_object" "telegram_handler_source" {
  name   = "telegram-handler-${data.archive_file.telegram_handler_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.telegram_handler_zip.output_path
}

resource "google_storage_bucket_object" "airtable_sync_source" {
  name   = "airtable-sync-${data.archive_file.airtable_sync_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.airtable_sync_zip.output_path
}

resource "google_storage_bucket_object" "followup_scheduler_source" {
  name   = "followup-scheduler-${data.archive_file.followup_scheduler_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.followup_scheduler_zip.output_path
}

# Telegram webhook handler Cloud Function
resource "google_cloudfunctions2_function" "telegram_handler" {
  name        = "telegram-voice-handler"
  location    = var.region
  description = "Handles Telegram voice messages and routes to ElevenLabs agent"

  build_config {
    runtime           = "python311"
    entry_point       = "telegram_handler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.telegram_handler_source.name
      }
    }
  }

  service_config {
    max_instance_count = 10
    min_instance_count = 0
    available_memory   = "512Mi"
    timeout_seconds    = 60
    
    service_account_email = google_service_account.function_service_account.email
    
    environment_variables = {
      PROJECT_ID = var.project_id
      AUDIO_BUCKET = google_storage_bucket.audio_files.name
    }
    
    secret_environment_variables {
      key        = "TELEGRAM_BOT_TOKEN"
      project_id = var.project_id
      secret     = google_secret_manager_secret.telegram_bot_token.secret_id
      version    = "latest"
    }
    
    secret_environment_variables {
      key        = "ELEVENLABS_API_KEY"
      project_id = var.project_id
      secret     = google_secret_manager_secret.elevenlabs_api_key.secret_id
      version    = "latest"
    }
    
    secret_environment_variables {
      key        = "ELEVENLABS_AGENT_ID"
      project_id = var.project_id
      secret     = google_secret_manager_secret.elevenlabs_agent_id.secret_id
      version    = "latest"
    }
    
  }

  depends_on = [
    google_project_service.required_apis,
    google_storage_bucket_object.telegram_handler_source,
    google_storage_bucket_object.airtable_sync_source,
    google_storage_bucket_object.followup_scheduler_source
  ]
}

# Allow public access to telegram handler
resource "google_cloudfunctions2_function_iam_member" "telegram_handler_invoker" {
  project        = var.project_id
  location       = google_cloudfunctions2_function.telegram_handler.location
  cloud_function = google_cloudfunctions2_function.telegram_handler.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}

# Airtable sync Cloud Function (triggered by Firestore changes)
resource "google_cloudfunctions2_function" "airtable_sync" {
  name        = "airtable-sync"
  location    = var.region
  description = "Syncs incident data from Firestore to Airtable"

  build_config {
    runtime           = "python311"
    entry_point       = "airtable_sync"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.airtable_sync_source.name
      }
    }
  }

  service_config {
    max_instance_count = 10
    min_instance_count = 0
    available_memory   = "256Mi"
    timeout_seconds    = 30
    
    service_account_email = google_service_account.function_service_account.email
    
    environment_variables = {
      PROJECT_ID = var.project_id
    }
    
    secret_environment_variables {
      key        = "AIRTABLE_API_KEY"
      project_id = var.project_id
      secret     = google_secret_manager_secret.airtable_pat.secret_id
      version    = "latest"
    }
    
    secret_environment_variables {
      key        = "AIRTABLE_BASE_ID"
      project_id = var.project_id
      secret     = google_secret_manager_secret.airtable_base_id.secret_id
      version    = "latest"
    }
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.firestore.document.v1.created"
    retry_policy   = "RETRY_POLICY_RETRY"
    
    event_filters {
      attribute = "database"
      value     = "(default)"
    }
    
    event_filters {
      attribute = "document"
      value     = "incidents/{incident_id}"
    }
  }

  depends_on = [
    google_project_service.required_apis,
    google_storage_bucket_object.telegram_handler_source,
    google_storage_bucket_object.airtable_sync_source,
    google_storage_bucket_object.followup_scheduler_source
  ]
}

# Follow-up scheduler Cloud Function
resource "google_cloudfunctions2_function" "followup_scheduler" {
  name        = "followup-scheduler"
  location    = var.region
  description = "Scheduled function to send follow-up messages for unresolved incidents"

  build_config {
    runtime           = "python311"
    entry_point       = "followup_scheduler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.followup_scheduler_source.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    min_instance_count = 0
    available_memory   = "512Mi"
    timeout_seconds    = 300
    
    service_account_email = google_service_account.function_service_account.email
    
    environment_variables = {
      PROJECT_ID = var.project_id
    }
    
    secret_environment_variables {
      key        = "TELEGRAM_BOT_TOKEN"
      project_id = var.project_id
      secret     = google_secret_manager_secret.telegram_bot_token.secret_id
      version    = "latest"
    }
    
    secret_environment_variables {
      key        = "ELEVENLABS_API_KEY"
      project_id = var.project_id
      secret     = google_secret_manager_secret.elevenlabs_api_key.secret_id
      version    = "latest"
    }
    
    secret_environment_variables {
      key        = "ELEVENLABS_AGENT_ID"
      project_id = var.project_id
      secret     = google_secret_manager_secret.elevenlabs_agent_id.secret_id
      version    = "latest"
    }
  }

  depends_on = [
    google_project_service.required_apis,
    google_storage_bucket_object.telegram_handler_source,
    google_storage_bucket_object.airtable_sync_source,
    google_storage_bucket_object.followup_scheduler_source
  ]
}

# Cloud Scheduler job for follow-ups
resource "google_cloud_scheduler_job" "followup_schedule" {
  name             = "followup-scheduler"
  description      = "Daily follow-up for unresolved incidents"
  schedule         = "0 9 * * *"  # Daily at 9 AM
  time_zone        = "America/New_York"
  attempt_deadline = "60s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.followup_scheduler.service_config[0].uri
  }

  depends_on = [google_project_service.required_apis]
}

# Outputs
output "telegram_webhook_url" {
  description = "URL for Telegram webhook"
  value       = google_cloudfunctions2_function.telegram_handler.service_config[0].uri
}

output "project_id" {
  description = "Google Cloud Project ID"
  value       = var.project_id
}

output "audio_bucket_name" {
  description = "Cloud Storage bucket for audio files"
  value       = google_storage_bucket.audio_files.name
}

output "service_account_email" {
  description = "Service account email for functions"
  value       = google_service_account.function_service_account.email
}

output "deployment_summary" {
  description = "Summary of deployed resources"
  value = {
    telegram_webhook_url = google_cloudfunctions2_function.telegram_handler.service_config[0].uri
    project_id          = var.project_id
    region              = var.region
    audio_bucket        = google_storage_bucket.audio_files.name
    functions_deployed  = [
      google_cloudfunctions2_function.telegram_handler.name,
      google_cloudfunctions2_function.airtable_sync.name,
      google_cloudfunctions2_function.followup_scheduler.name
    ]
  }
}