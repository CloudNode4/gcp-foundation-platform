output "folder_ids" {
  description = "Created folder IDs keyed by logical folder name."
  value       = module.folders.folder_ids
}

output "project_ids" {
  description = "Created project IDs keyed by logical project name."
  value       = module.projects.project_ids
}

output "shared_vpc_networks" {
  description = "Shared VPC network self links keyed by logical network name."
  value       = module.shared_vpc.network_self_links
}

output "audit_log_sink_writer_identity" {
  description = "Writer identity for the organization audit log sink."
  value       = try(module.logging[0].sink_writer_identity, null)
}

output "monitoring_notification_channels" {
  description = "Monitoring notification channel IDs."
  value       = try(module.monitoring[0].notification_channel_ids, {})
}
