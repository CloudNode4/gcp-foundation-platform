output "project_ids" {
  description = "Project IDs keyed by logical project name."
  value       = { for key, project in google_project.this : key => project.project_id }
}

output "project_numbers" {
  description = "Project numbers keyed by logical project name."
  value       = { for key, project in google_project.this : key => project.number }
}
