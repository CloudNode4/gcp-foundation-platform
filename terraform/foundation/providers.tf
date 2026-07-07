provider "google" {
  region              = var.default_region
  user_project_override = true
}

provider "google-beta" {
  region              = var.default_region
  user_project_override = true
}
