output "notification_channel_ids" {
  description = "Notification channel IDs keyed by logical channel name."
  value       = { for key, channel in google_monitoring_notification_channel.email : key => channel.name }
}
