locals {
  email_channels = {
    for channel in var.notification_channels : channel.name => channel
    if channel.type == "email"
  }
}

resource "google_monitoring_notification_channel" "email" {
  for_each = local.email_channels

  project      = var.project_id
  display_name = each.value.display_name
  type         = "email"

  labels = {
    email_address = each.value.email
  }
}
