from __future__ import annotations

import ipaddress
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

PROJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")
LABEL_KEY_RE = re.compile(r"^[a-z][a-z0-9_-]{0,62}$")
BILLING_ACCOUNT_RE = re.compile(r"^[A-Fa-f0-9]{6}-[A-Fa-f0-9]{6}-[A-Fa-f0-9]{6}$")
IAM_MEMBER_RE = re.compile(
    r"^(user|group|serviceAccount|domain|principal|principalSet|allUsers|allAuthenticatedUsers)(:|$).+|^(allUsers|allAuthenticatedUsers)$"
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class FolderConfig(StrictModel):
    display_name: str = Field(min_length=1, max_length=64)
    parent: str | None = Field(
        default=None,
        description="Optional full parent resource name, for example folders/123456789.",
    )


class ProjectConfig(StrictModel):
    project_id: str
    name: str = Field(min_length=1, max_length=30)
    folder: str = Field(min_length=1)
    services: list[str] = Field(default_factory=list)
    labels: dict[str, str] = Field(default_factory=dict)
    deletion_policy: Literal["PREVENT", "DELETE", "ABANDON"] = "PREVENT"

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not PROJECT_ID_RE.fullmatch(value):
            raise ValueError(
                "project_id must be 6-30 chars, start with a lowercase letter, "
                "and contain only lowercase letters, digits, or hyphens"
            )
        return value

    @field_validator("services")
    @classmethod
    def validate_services(cls, values: list[str]) -> list[str]:
        for service in values:
            if not service.endswith(".googleapis.com"):
                raise ValueError(f"Invalid Google API service name: {service}")
        return sorted(set(values))

    @field_validator("labels")
    @classmethod
    def validate_project_labels(cls, labels: dict[str, str]) -> dict[str, str]:
        return validate_labels(labels)


class SubnetConfig(StrictModel):
    name: str = Field(min_length=1, max_length=63)
    region: str = Field(min_length=1)
    ip_cidr_range: str
    private_ip_google_access: bool = True
    secondary_ip_ranges: dict[str, str] = Field(default_factory=dict)

    @field_validator("ip_cidr_range")
    @classmethod
    def validate_primary_cidr(cls, value: str) -> str:
        ipaddress.ip_network(value)
        return value

    @field_validator("secondary_ip_ranges")
    @classmethod
    def validate_secondary_ranges(cls, values: dict[str, str]) -> dict[str, str]:
        for name, cidr in values.items():
            if not name:
                raise ValueError("secondary range name cannot be empty")
            ipaddress.ip_network(cidr)
        return values


class NatConfig(StrictModel):
    enabled: bool = True
    region: str


class NetworkConfig(StrictModel):
    host_project: str
    description: str = "Managed by Terraform."
    auto_create_subnetworks: bool = False
    subnets: list[SubnetConfig] = Field(default_factory=list)
    nat: NatConfig | None = None

    @model_validator(mode="after")
    def validate_unique_subnets(self) -> "NetworkConfig":
        names = [subnet.name for subnet in self.subnets]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(f"Duplicate subnet names: {', '.join(duplicates)}")
        return self


class ListPolicyConfig(StrictModel):
    allowed_values: list[str] = Field(default_factory=list)
    denied_values: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_values(self) -> "ListPolicyConfig":
        if not self.allowed_values and not self.denied_values:
            raise ValueError("list policy must define at least one allowed or denied value")
        overlap = set(self.allowed_values).intersection(self.denied_values)
        if overlap:
            raise ValueError(f"policy values cannot be both allowed and denied: {sorted(overlap)}")
        return self


class OrgPoliciesConfig(StrictModel):
    boolean: dict[str, bool] = Field(default_factory=dict)
    list: dict[str, ListPolicyConfig] = Field(default_factory=dict)


class IAMConfig(StrictModel):
    organization: dict[str, list[str]] = Field(default_factory=dict)
    folders: dict[str, dict[str, list[str]]] = Field(default_factory=dict)
    projects: dict[str, dict[str, list[str]]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_members(self) -> "IAMConfig":
        for scope_name, bindings in self.organization.items():
            validate_iam_binding(scope_name, bindings)
        for folder_bindings in self.folders.values():
            for role, members in folder_bindings.items():
                validate_iam_binding(role, members)
        for project_bindings in self.projects.values():
            for role, members in project_bindings.items():
                validate_iam_binding(role, members)
        return self


class LoggingConfig(StrictModel):
    audit_logs_project: str
    audit_logs_bucket: str = Field(min_length=3, max_length=63)
    location: str = "EU"
    retention_days: int = Field(default=365, ge=1, le=3650)


class NotificationChannelConfig(StrictModel):
    name: str
    display_name: str
    type: Literal["email"] = "email"
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email notification channel must contain @")
        return value


class MonitoringConfig(StrictModel):
    project: str
    notification_channels: list[NotificationChannelConfig] = Field(default_factory=list)


class FoundationConfig(StrictModel):
    organization_id: str
    billing_account: str
    default_region: str = "europe-west1"
    labels: dict[str, str] = Field(default_factory=dict)
    folders: dict[str, FolderConfig] = Field(default_factory=dict)
    projects: dict[str, ProjectConfig] = Field(default_factory=dict)
    networks: dict[str, NetworkConfig] = Field(default_factory=dict)
    iam: IAMConfig = Field(default_factory=IAMConfig)
    org_policies: OrgPoliciesConfig = Field(default_factory=OrgPoliciesConfig)
    logging: LoggingConfig | None = None
    monitoring: MonitoringConfig | None = None

    @field_validator("organization_id")
    @classmethod
    def validate_org_id(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("organization_id must be numeric")
        return value

    @field_validator("billing_account")
    @classmethod
    def validate_billing_account(cls, value: str) -> str:
        if not BILLING_ACCOUNT_RE.fullmatch(value):
            raise ValueError("billing_account must look like 000000-000000-000000")
        return value.upper()

    @field_validator("labels")
    @classmethod
    def validate_global_labels(cls, labels: dict[str, str]) -> dict[str, str]:
        return validate_labels(labels)

    @model_validator(mode="after")
    def validate_references(self) -> "FoundationConfig":
        folder_keys = set(self.folders)
        project_keys = set(self.projects)

        for project_key, project in self.projects.items():
            if project.folder not in folder_keys and not project.folder.startswith("folders/"):
                raise ValueError(
                    f"project '{project_key}' references unknown folder '{project.folder}'"
                )

        for network_key, network in self.networks.items():
            if network.host_project not in project_keys and not network.host_project.startswith("projects/"):
                raise ValueError(
                    f"network '{network_key}' references unknown host project "
                    f"'{network.host_project}'"
                )

        for folder_key in self.iam.folders:
            if folder_key not in folder_keys and not folder_key.startswith("folders/"):
                raise ValueError(f"IAM references unknown folder '{folder_key}'")

        for project_key in self.iam.projects:
            if project_key not in project_keys and not project_key.startswith("projects/"):
                raise ValueError(f"IAM references unknown project '{project_key}'")

        if self.logging and self.logging.audit_logs_project not in project_keys:
            raise ValueError(
                "logging.audit_logs_project references unknown project "
                f"'{self.logging.audit_logs_project}'"
            )

        if self.monitoring and self.monitoring.project not in project_keys:
            raise ValueError(
                f"monitoring.project references unknown project '{self.monitoring.project}'"
            )

        return self


def validate_labels(labels: dict[str, str]) -> dict[str, str]:
    for key, value in labels.items():
        if not LABEL_KEY_RE.fullmatch(key):
            raise ValueError(f"Invalid label key: {key}")
        if len(value) > 63:
            raise ValueError(f"Label value for '{key}' must be <= 63 characters")
    return labels


def validate_iam_binding(role: str, members: list[str]) -> None:
    if not role.startswith("roles/") and not role.startswith("organizations/") and not role.startswith("projects/"):
        raise ValueError(f"Invalid IAM role name: {role}")
    for member in members:
        if not IAM_MEMBER_RE.match(member):
            raise ValueError(f"Invalid IAM member: {member}")


def load_config(path: str | Path) -> FoundationConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Configuration file must contain a YAML object at the top level")

    try:
        return FoundationConfig.model_validate(raw)
    except ValidationError:
        raise


def to_tfvars(config: FoundationConfig) -> dict[str, Any]:
    return {
        "organization_id": config.organization_id,
        "billing_account": config.billing_account,
        "default_region": config.default_region,
        "labels": config.labels,
        "folders": {key: value.model_dump(exclude_none=True) for key, value in config.folders.items()},
        "projects": {key: value.model_dump() for key, value in config.projects.items()},
        "networks": {key: value.model_dump(exclude_none=True) for key, value in config.networks.items()},
        "iam_bindings": config.iam.model_dump(),
        "org_policies": config.org_policies.model_dump(),
        "logging": config.logging.model_dump() if config.logging else None,
        "monitoring": config.monitoring.model_dump() if config.monitoring else None,
    }
