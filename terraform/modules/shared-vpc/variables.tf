variable "networks" {
  description = "Shared VPC networks keyed by logical network name."
  type = map(object({
    host_project_id         = string
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
