variable "organization_id" {
  description = "Numeric Google Cloud organization ID."
  type        = string
}

variable "folder_ids" {
  description = "Folder IDs keyed by logical folder name."
  type        = map(string)
  default     = {}
}

variable "project_ids" {
  description = "Project IDs keyed by logical project name."
  type        = map(string)
  default     = {}
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
