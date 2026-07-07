locals {
  folder_ids = module.folders.folder_ids
  project_ids = module.projects.project_ids

  projects = {
    for key, project in var.projects : key => merge(project, {
      folder_id = contains(keys(local.folder_ids), project.folder) ? local.folder_ids[project.folder] : replace(project.folder, "folders/", "")
      labels    = merge(var.labels, try(project.labels, {}))
    })
  }

  networks = {
    for key, network in var.networks : key => merge(network, {
      host_project_id = contains(keys(local.project_ids), network.host_project) ? local.project_ids[network.host_project] : replace(network.host_project, "projects/", "")
    })
  }

  logging_config = var.logging == null ? null : merge(var.logging, {
    audit_logs_project_id = contains(keys(local.project_ids), var.logging.audit_logs_project) ? local.project_ids[var.logging.audit_logs_project] : replace(var.logging.audit_logs_project, "projects/", "")
  })

  monitoring_config = var.monitoring == null ? null : merge(var.monitoring, {
    project_id = contains(keys(local.project_ids), var.monitoring.project) ? local.project_ids[var.monitoring.project] : replace(var.monitoring.project, "projects/", "")
  })
}
