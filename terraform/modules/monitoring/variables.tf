variable "project_id" {
  description = "Monitoring project ID."
  type        = string
}

variable "notification_channels" {
  description = "Notification channels. Currently supports email channels."
  type = list(object({
    name         = string
    display_name = string
    type         = string
    email        = string
  }))
  default = []
}
