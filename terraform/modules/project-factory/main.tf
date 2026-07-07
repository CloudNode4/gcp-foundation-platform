resource "google_project" "this" {
  for_each = var.projects

  name                = each.value.name
  project_id          = each.value.project_id
  folder_id           = each.value.folder_id
  billing_account     = var.billing_account
  auto_create_network = false
  labels              = try(each.value.labels, {})
  deletion_policy     = try(each.value.deletion_policy, "PREVENT")
}

locals {
  project_services = {
    for item in flatten([
      for project_key, project in var.projects : [
        for service in try(project.services, []) : {
          key         = "${project_key}/${service}"
          project_key = project_key
          service     = service
        }
      ]
    ]) : item.key => item
  }
}

resource "google_project_service" "enabled" {
  for_each = local.project_services

  project            = google_project.this[each.value.project_key].project_id
  service            = each.value.service
  disable_on_destroy = false
}
