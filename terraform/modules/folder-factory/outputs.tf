output "folder_ids" {
  description = "Numeric folder IDs keyed by logical folder name."
  value       = { for key, folder in google_folder.this : key => folder.folder_id }
}

output "folder_names" {
  description = "Full folder resource names keyed by logical folder name."
  value       = { for key, folder in google_folder.this : key => folder.name }
}
