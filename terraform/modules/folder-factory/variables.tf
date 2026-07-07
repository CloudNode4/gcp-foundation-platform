variable "organization_id" {
  description = "Numeric Google Cloud organization ID."
  type        = string
}

variable "folders" {
  description = "Folders keyed by logical name."
  type = map(object({
    display_name = string
    parent       = optional(string)
  }))
  default = {}
}
