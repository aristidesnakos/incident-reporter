output "deployment_summary" {
  description = "Summary of deployed infrastructure"
  value = {
    telegram_webhook_url  = google_cloudfunctions2_function.telegram_handler.service_config[0].uri
    project_id           = var.project_id
    region               = var.region
    audio_bucket         = google_storage_bucket.audio_files.name
    functions_deployed   = [
      google_cloudfunctions2_function.telegram_handler.name,
      google_cloudfunctions2_function.airtable_sync.name,
      google_cloudfunctions2_function.followup_scheduler.name
    ]
    service_account_email = google_service_account.function_service_account.email
  }
}

output "telegram_webhook_url" {
  description = "URL for Telegram webhook configuration"
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

output "next_steps" {
  description = "Next steps after infrastructure deployment"
  value = [
    "1. Set Telegram webhook:",
    "   curl -F \"url=${google_cloudfunctions2_function.telegram_handler.service_config[0].uri}\" https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook",
    "2. Test voice message to Telegram bot",
    "3. Check Cloud Functions logs: gcloud functions logs read telegram-voice-handler --region=${var.region}",
    "4. Monitor Airtable dashboard for real-time incident data",
    "5. Verify ElevenLabs agent responses are working"
  ]
}

output "service_endpoints" {
  description = "Important service endpoints and resources"
  value = {
    telegram_webhook     = google_cloudfunctions2_function.telegram_handler.service_config[0].uri
    firestore_database  = google_firestore_database.database.name
    storage_bucket_url  = "gs://${google_storage_bucket.audio_files.name}"
    functions_region    = var.region
    scheduler_job       = google_cloud_scheduler_job.followup_schedule.name
  }
}

output "monitoring_links" {
  description = "Links to monitoring and debugging resources"
  value = [
    "Cloud Functions Console: https://console.cloud.google.com/functions/list?project=${var.project_id}",
    "Firestore Console: https://console.cloud.google.com/firestore/data?project=${var.project_id}",
    "Cloud Scheduler Console: https://console.cloud.google.com/cloudscheduler?project=${var.project_id}",
    "Logs Explorer: https://console.cloud.google.com/logs?project=${var.project_id}",
    "Secret Manager: https://console.cloud.google.com/security/secret-manager?project=${var.project_id}"
  ]
}

output "cost_estimates" {
  description = "Estimated costs for development and production"
  value = {
    development_24h = "~$5 total (Cloud Functions: $1, ElevenLabs: $3, Storage: $1)"
    production_monthly = "~$20-50 depending on usage (serverless scales with demand)"
    cost_breakdown = [
      "Cloud Functions: $0.0000004 per invocation + $0.0000025 per GB-second",
      "Firestore: $0.18 per 100K reads, $0.54 per 100K writes",
      "Cloud Storage: $0.026 per GB per month",
      "ElevenLabs: ~$0.20-0.30 per 1000 characters (voice generation)",
      "Cloud Scheduler: $0.10 per job per month"
    ]
  }
}

output "template_info" {
  description = "Information about reusable template components"
  value = {
    template_type = "Serverless Conversational AI Voice Processing"
    reusability_score = "High - suitable for other voice-enabled applications"
    deployment_time = "3-5 minutes with ./deploy.sh"
    customization_points = [
      "ElevenLabs agent prompts (change domain/use case)",
      "Firestore data schema (add/modify fields)",
      "Airtable base structure (different dashboard needs)",
      "Follow-up schedule (adjust timing)",
      "Urgency classification logic (different alert thresholds)"
    ]
    future_hackathon_ready = true
  }
}