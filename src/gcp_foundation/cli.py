from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel

from gcp_foundation.config import load_config
from gcp_foundation.generator import write_tfvars
from gcp_foundation.inventory import render_inventory
from gcp_foundation.terraform import build_command, require_terraform, run_command
from gcp_foundation.validators import check_repo_structure

app = typer.Typer(
    name="gcp-foundation",
    help="Automation CLI for the GCP Foundation Platform repository.",
    no_args_is_help=True,
)
console = Console()


@app.command("validate-config")
def validate_config(
    config: Annotated[Path, typer.Option("--config", "-c", exists=True, readable=True)],
) -> None:
    """Validate an organization YAML configuration file."""
    try:
        loaded = load_config(config)
    except ValidationError as exc:
        console.print("[bold red]Configuration validation failed[/bold red]")
        console.print(exc)
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(f"[bold red]Failed to load config:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(
        Panel.fit(
            f"Organization: {loaded.organization_id}\n"
            f"Folders: {len(loaded.folders)}\n"
            f"Projects: {len(loaded.projects)}\n"
            f"Networks: {len(loaded.networks)}",
            title="Config OK",
            border_style="green",
        )
    )


@app.command("generate-tfvars")
def generate_tfvars(
    config: Annotated[Path, typer.Option("--config", "-c", exists=True, readable=True)],
    output: Annotated[Path, typer.Option("--output", "-o")],
) -> None:
    """Generate Terraform tfvars JSON from an organization YAML config."""
    try:
        loaded = load_config(config)
        path = write_tfvars(loaded, output)
    except Exception as exc:
        console.print(f"[bold red]Failed to generate tfvars:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]Generated[/green] {path}")


@app.command("inventory")
def inventory(
    config: Annotated[Path, typer.Option("--config", "-c", exists=True, readable=True)],
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
) -> None:
    """Render a Markdown inventory from an organization YAML config."""
    try:
        loaded = load_config(config)
        markdown = render_inventory(loaded)
    except Exception as exc:
        console.print(f"[bold red]Failed to render inventory:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
        console.print(f"[green]Generated[/green] {output}")
    else:
        console.print(markdown)


@app.command("check-repo")
def check_repo(
    path: Annotated[Path, typer.Option("--path", "-p", exists=True)] = Path("."),
) -> None:
    """Check that the repository contains the expected production-grade files."""
    result = check_repo_structure(path)
    if result.ok:
        console.print("[green]Repository structure OK[/green]")
        return

    if result.missing_paths:
        console.print("[bold red]Missing required paths:[/bold red]")
        for missing in result.missing_paths:
            console.print(f"  - {missing}")
    if result.forbidden_paths:
        console.print("[bold red]Forbidden generated/state files present:[/bold red]")
        for forbidden in result.forbidden_paths:
            console.print(f"  - {forbidden}")
    raise typer.Exit(code=1)


@app.command("terraform")
def terraform(
    action: Annotated[str, typer.Option("--action", "-a")],
    workdir: Annotated[Path, typer.Option("--workdir", "-w")] = Path("terraform/foundation"),
    var_file: Annotated[str | None, typer.Option("--var-file")] = None,
    auto_approve: Annotated[bool, typer.Option("--auto-approve")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Run or print a Terraform command for the foundation root module."""
    try:
        terraform_bin = "terraform" if dry_run else require_terraform()
        command = build_command(
            action=action,
            workdir=workdir,
            var_file=var_file,
            auto_approve=auto_approve,
            terraform_bin=terraform_bin,
        )
    except Exception as exc:
        console.print(f"[bold red]Invalid Terraform command:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(" ".join(command.as_list()))
    if dry_run:
        return

    code = run_command(command)
    raise typer.Exit(code=code)
