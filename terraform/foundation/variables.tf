variable "organization_id" {
  description = "Numeric Google Cloud organization ID."
  type        = string
}

variable "billing_account" {
  description = "Billing account ID attached to created projects."
  type        = string
}

variable "default_region" {
  description = "Default Google Cloud region."
  type        = string
  default     = "europe-west1"
}

variable "labels" {
  description = "Global labels applied to supported resources."
  type        = map(string)
  default     = {}
}

variable "folders" {
  description = "Folder definitions keyed by logical folder name."
  type = map(object({
    display_name = string
    parent       = optional(string)
  }))
  default = {}
}

variable "projects" {
  description = "Project definitions keyed by logical project name."
  type = map(object({
    project_id      = string
    name            = string
    folder          = string
    services        = optional(list(string), [])
    labels          = optional(map(string), {})
    deletion_policy = optional(string, "PREVENT")
  }))
  default = {}
}

variable "networks" {
  description = "Shared VPC network definitions."
  type = map(object({
    host_project            = string
    description             = optional(string, "Managed by Terraform.")
    auto_create_subnetworks = optional(bool, false)
    subnets = optional(list(object({
      name                     = string
      region                   = string
      ip_cidr_range            = string
      private_ip_google_access = optional(bool, true)
      secondary_ip_ranges      = optional(map(string), {})
    })), [])
    nat = optional(object({
      enabled = bool
      region  = string
    }))
  }))
  default = {}
}

variable "iam_bindings" {
  description = "IAM member bindings for organization, folders, and projects."
  type = object({
    organization = optional(map(list(string)), {})
    folders      = optional(map(map(list(string))), {})
    projects     = optional(map(map(list(string))), {})
  })
  default = {}
}

variable "org_policies" {
  description = "Organization policy definitions."
  type = object({
    boolean = optional(map(bool), {})
    list = optional(map(object({
      allowed_values = optional(list(string), [])
      denied_values  = optional(list(string), [])
    })), {})
  })
  default = {}
}

variable "logging" {
  description = "Centralized organization audit logging configuration."
  type = object({
    audit_logs_project = string
    audit_logs_bucket  = string
    location           = optional(string, "EU")
    retention_days     = optional(number, 365)
  })
  default = null
}

variable "monitoring" {
  description = "Monitoring configuration."
  type = object({
    project = string
    notification_channels = optional(list(object({
      name         = string
      display_name = string
      type         = string
      email        = string
    })), [])
  })
  default = null
}
