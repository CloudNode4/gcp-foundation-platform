resource "google_storage_bucket" "audit_logs" {
  name                        = var.bucket_name
  project                     = var.project_id
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = false

  versioning {
    enabled = true
  }

  retention_policy {
    retention_period = var.retention_days * 24 * 60 * 60
    is_locked        = false
  }
}

resource "google_logging_organization_sink" "audit" {
  name             = "foundation-audit-logs"
  org_id           = var.organization_id
  destination      = "storage.googleapis.com/${google_storage_bucket.audit_logs.name}"
  include_children = true

  filter = <<-EOT
    logName:"/logs/cloudaudit.googleapis.com%2Factivity" OR
    logName:"/logs/cloudaudit.googleapis.com%2Fsystem_event" OR
    logName:"/logs/cloudaudit.googleapis.com%2Fpolicy"
  EOT
}

resource "google_storage_bucket_iam_member" "sink_writer" {
  bucket = google_storage_bucket.audit_logs.name
  role   = "roles/storage.objectCreator"
  member = google_logging_organization_sink.audit.writer_identity
}
