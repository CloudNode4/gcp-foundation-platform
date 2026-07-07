output "bucket_name" {
  description = "Audit log bucket name."
  value       = google_storage_bucket.audit_logs.name
}

output "sink_name" {
  description = "Organization log sink name."
  value       = google_logging_organization_sink.audit.name
}

output "sink_writer_identity" {
  description = "Writer identity of the organization log sink."
  value       = google_logging_organization_sink.audit.writer_identity
}
