locals {
  host_projects = toset(distinct([for _, network in var.networks : network.host_project_id]))

  subnets = {
    for item in flatten([
      for network_key, network in var.networks : [
        for subnet in try(network.subnets, []) : {
          key                      = "${network_key}/${subnet.name}"
          network_key              = network_key
          host_project_id          = network.host_project_id
          name                     = subnet.name
          region                   = subnet.region
          ip_cidr_range            = subnet.ip_cidr_range
          private_ip_google_access = try(subnet.private_ip_google_access, true)
          secondary_ip_ranges      = try(subnet.secondary_ip_ranges, {})
        }
      ]
    ]) : item.key => item
  }

  nats = {
    for key, network in var.networks : key => network
    if try(network.nat.enabled, false)
  }
}

resource "google_compute_shared_vpc_host_project" "this" {
  for_each = local.host_projects

  project = each.value
}

resource "google_compute_network" "this" {
  for_each = var.networks

  name                    = each.key
  project                 = each.value.host_project_id
  description             = try(each.value.description, "Managed by Terraform.")
  auto_create_subnetworks = try(each.value.auto_create_subnetworks, false)

  depends_on = [google_compute_shared_vpc_host_project.this]
}

resource "google_compute_subnetwork" "this" {
  for_each = local.subnets

  name                     = each.value.name
  project                  = each.value.host_project_id
  region                   = each.value.region
  network                  = google_compute_network.this[each.value.network_key].self_link
  ip_cidr_range            = each.value.ip_cidr_range
  private_ip_google_access = each.value.private_ip_google_access

  dynamic "secondary_ip_range" {
    for_each = each.value.secondary_ip_ranges
    content {
      range_name    = secondary_ip_range.key
      ip_cidr_range = secondary_ip_range.value
    }
  }
}

resource "google_compute_router" "nat" {
  for_each = local.nats

  name    = "${each.key}-nat-router"
  project = each.value.host_project_id
  region  = each.value.nat.region
  network = google_compute_network.this[each.key].self_link
}

resource "google_compute_router_nat" "this" {
  for_each = local.nats

  name                               = "${each.key}-nat"
  project                            = each.value.host_project_id
  region                             = each.value.nat.region
  router                             = google_compute_router.nat[each.key].name
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
