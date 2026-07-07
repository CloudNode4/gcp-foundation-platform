output "organization_bindings" {
  description = "Organization IAM bindings created by this module."
  value       = keys(google_organization_iam_member.this)
}

output "folder_bindings" {
  description = "Folder IAM bindings created by this module."
  value       = keys(google_folder_iam_member.this)
}

output "project_bindings" {
  description = "Project IAM bindings created by this module."
  value       = keys(google_project_iam_member.this)
}
