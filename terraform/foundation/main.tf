module "folders" {
  source = "../modules/folder-factory"

  organization_id = var.organization_id
  folders         = var.folders
}

module "projects" {
  source = "../modules/project-factory"

  billing_account = var.billing_account
  projects        = local.projects
}

module "shared_vpc" {
  source = "../modules/shared-vpc"

  networks = local.networks

  depends_on = [module.projects]
}

module "iam" {
  source = "../modules/iam-bindings"

  organization_id = var.organization_id
  folder_ids      = module.folders.folder_ids
  project_ids     = module.projects.project_ids
  iam_bindings    = var.iam_bindings

  depends_on = [module.folders, module.projects]
}

module "org_policies" {
  source = "../modules/org-policies"

  organization_id  = var.organization_id
  boolean_policies = try(var.org_policies.boolean, {})
  list_policies    = try(var.org_policies.list, {})
}

module "logging" {
  count  = local.logging_config == null ? 0 : 1
  source = "../modules/logging"

  organization_id = var.organization_id
  project_id      = local.logging_config.audit_logs_project_id
  bucket_name     = local.logging_config.audit_logs_bucket
  location        = local.logging_config.location
  retention_days  = local.logging_config.retention_days

  depends_on = [module.projects]
}

module "monitoring" {
  count  = local.monitoring_config == null ? 0 : 1
  source = "../modules/monitoring"

  project_id             = local.monitoring_config.project_id
  notification_channels = try(local.monitoring_config.notification_channels, [])

  depends_on = [module.projects]
}
