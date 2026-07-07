locals {
  organization_parent = "organizations/${var.organization_id}"
}

resource "google_folder" "this" {
  for_each = var.folders

  display_name = each.value.display_name
  parent       = coalesce(try(each.value.parent, null), local.organization_parent)

  deletion_protection = true
}
