variable "billing_account" {
  description = "Billing account ID attached to created projects."
  type        = string
}

variable "projects" {
  description = "Project definitions keyed by logical project name."
  type = map(object({
    project_id      = string
    name            = string
    folder_id       = string
    services        = optional(list(string), [])
    labels          = optional(map(string), {})
    deletion_policy = optional(string, "PREVENT")
  }))
  default = {}
}
