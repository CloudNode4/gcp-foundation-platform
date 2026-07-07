variable "organization_id" {
  description = "Numeric Google Cloud organization ID."
  type        = string
}

variable "project_id" {
  description = "Project that owns the audit log bucket."
  type        = string
}

variable "bucket_name" {
  description = "Cloud Storage bucket name for audit logs."
  type        = string
}

variable "location" {
  description = "Bucket location."
  type        = string
  default     = "EU"
}

variable "retention_days" {
  description = "Audit log bucket retention in days."
  type        = number
  default     = 365
}
