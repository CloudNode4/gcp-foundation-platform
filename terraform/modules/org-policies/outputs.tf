output "boolean_policy_names" {
  description = "Boolean policy resource names."
  value       = { for key, policy in google_org_policy_policy.boolean : key => policy.name }
}

output "list_policy_names" {
  description = "List policy resource names."
  value       = { for key, policy in google_org_policy_policy.list : key => policy.name }
}
