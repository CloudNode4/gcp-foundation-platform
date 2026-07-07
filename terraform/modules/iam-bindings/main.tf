locals {
  organization_members = {
    for item in flatten([
      for role, members in try(var.iam_bindings.organization, {}) : [
        for member in members : {
          key    = "${role}/${member}"
          role   = role
          member = member
        }
      ]
    ]) : item.key => item
  }

  folder_members = {
    for item in flatten([
      for folder_key, role_map in try(var.iam_bindings.folders, {}) : [
        for role, members in role_map : [
          for member in members : {
            key        = "${folder_key}/${role}/${member}"
            folder_key = folder_key
            role       = role
            member     = member
          }
        ]
      ]
    ]) : item.key => item
  }

  project_members = {
    for item in flatten([
      for project_key, role_map in try(var.iam_bindings.projects, {}) : [
        for role, members in role_map : [
          for member in members : {
            key         = "${project_key}/${role}/${member}"
            project_key = project_key
            role        = role
            member      = member
          }
        ]
      ]
    ]) : item.key => item
  }
}

resource "google_organization_iam_member" "this" {
  for_each = local.organization_members

  org_id = var.organization_id
  role   = each.value.role
  member = each.value.member
}

resource "google_folder_iam_member" "this" {
  for_each = local.folder_members

  folder = contains(keys(var.folder_ids), each.value.folder_key) ? "folders/${var.folder_ids[each.value.folder_key]}" : each.value.folder_key
  role   = each.value.role
  member = each.value.member
}

resource "google_project_iam_member" "this" {
  for_each = local.project_members

  project = contains(keys(var.project_ids), each.value.project_key) ? var.project_ids[each.value.project_key] : replace(each.value.project_key, "projects/", "")
  role    = each.value.role
  member  = each.value.member
}
