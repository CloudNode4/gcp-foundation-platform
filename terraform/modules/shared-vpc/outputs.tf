output "network_self_links" {
  description = "Network self links keyed by logical network name."
  value       = { for key, network in google_compute_network.this : key => network.self_link }
}

output "subnet_self_links" {
  description = "Subnetwork self links keyed by network/subnet key."
  value       = { for key, subnet in google_compute_subnetwork.this : key => subnet.self_link }
}
