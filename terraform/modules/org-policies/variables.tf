variable "organization_id" {
  description = "Numeric Google Cloud organization ID."
  type        = string
}

variable "boolean_policies" {
  description = "Boolean organization policies keyed by full constraint name."
  type        = map(bool)
  default     = {}
}

variable "list_policies" {
  description = "List organization policies keyed by full constraint name."
  type = map(object({
    allowed_values = optional(list(string), [])
    denied_values  = optional(list(string), [])
  }))
  default = {}
}
