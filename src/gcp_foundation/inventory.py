from __future__ import annotations

from gcp_foundation.config import FoundationConfig


def render_inventory(config: FoundationConfig) -> str:
    lines: list[str] = [
        "# GCP Foundation Inventory",
        "",
        f"Organization ID: `{config.organization_id}`",
        f"Default region: `{config.default_region}`",
        "",
        "## Folders",
        "",
        "| Key | Display name | Parent |",
        "|---|---|---|",
    ]

    for key, folder in sorted(config.folders.items()):
        lines.append(
            f"| `{key}` | {folder.display_name} | `{folder.parent or 'organization root'}` |"
        )

    lines.extend(
        [
            "",
            "## Projects",
            "",
            "| Key | Project ID | Folder | Services |",
            "|---|---|---|---|",
        ]
    )

    for key, project in sorted(config.projects.items()):
        services = "<br>".join(project.services) if project.services else "-"
        lines.append(f"| `{key}` | `{project.project_id}` | `{project.folder}` | {services} |")

    lines.extend(
        [
            "",
            "## Networks",
            "",
            "| Key | Host project | Subnets | NAT |",
            "|---|---|---|---|",
        ]
    )

    for key, network in sorted(config.networks.items()):
        subnets = (
            "<br>".join(
                f"`{subnet.name}` `{subnet.region}` `{subnet.ip_cidr_range}`"
                for subnet in network.subnets
            )
            or "-"
        )
        nat = "enabled" if network.nat and network.nat.enabled else "disabled"
        lines.append(f"| `{key}` | `{network.host_project}` | {subnets} | {nat} |")

    lines.extend(
        [
            "",
            "## Organization policies",
            "",
            "### Boolean policies",
            "",
            "| Constraint | Enforced |",
            "|---|---|",
        ]
    )

    for constraint, enforced in sorted(config.org_policies.boolean.items()):
        lines.append(f"| `{constraint}` | `{enforced}` |")

    lines.extend(
        [
            "",
            "### List policies",
            "",
            "| Constraint | Allowed values | Denied values |",
            "|---|---|---|",
        ]
    )

    for constraint, policy in sorted(config.org_policies.list.items()):
        allowed = ", ".join(f"`{value}`" for value in policy.allowed_values) or "-"
        denied = ", ".join(f"`{value}`" for value in policy.denied_values) or "-"
        lines.append(f"| `{constraint}` | {allowed} | {denied} |")

    if config.logging:
        lines.extend(
            [
                "",
                "## Logging",
                "",
                f"Audit logs project: `{config.logging.audit_logs_project}`",
                f"Audit logs bucket: `{config.logging.audit_logs_bucket}`",
                f"Retention days: `{config.logging.retention_days}`",
            ]
        )

    if config.monitoring:
        lines.extend(
            [
                "",
                "## Monitoring",
                "",
                f"Monitoring project: `{config.monitoring.project}`",
                "",
                "| Channel | Type | Target |",
                "|---|---|---|",
            ]
        )
        for channel in config.monitoring.notification_channels:
            lines.append(f"| `{channel.name}` | `{channel.type}` | `{channel.email}` |")

    return "\n".join(lines) + "\n"
