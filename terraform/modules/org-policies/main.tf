locals {
  parent = "organizations/${var.organization_id}"
}

resource "google_org_policy_policy" "boolean" {
  for_each = var.boolean_policies

  name   = "${local.parent}/policies/${replace(each.key, "constraints/", "")}"
  parent = local.parent

  spec {
    rules {
      enforce = each.value ? "TRUE" : "FALSE"
    }
  }
}

resource "google_org_policy_policy" "list" {
  for_each = var.list_policies

  name   = "${local.parent}/policies/${replace(each.key, "constraints/", "")}"
  parent = local.parent

  spec {
    rules {
      values {
        allowed_values = try(each.value.allowed_values, [])
        denied_values  = try(each.value.denied_values, [])
      }
    }
  }
}
