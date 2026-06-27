import typer
from rich.console import Console
from rich.table import Table
from kubectl_ai.ai import ask_ai
from kubectl_ai.kubernetes import (
    get_pods,
    get_pod,
    get_pod_logs,
)

from kubectl_ai.kubernetes import get_pods

app = typer.Typer(
    help="🤖 AI-powered kubectl plugin for Kubernetes troubleshooting."
)

console = Console()

@app.command()
def ask(question: str):
    """Ask AI about Kubernetes."""

    console.print("[bold green]Thinking...[/bold green]")

    answer = ask_ai(question)

    console.print(answer)


@app.command()
def version():
    """Show plugin version."""
    console.print("[bold green]Kubectl AI Plugin[/bold green]")
    console.print("Version: 0.1.0")

@app.command()
def describe(pod: str):
    """Describe a pod."""

    namespace = "kube-system"

    pod_info = get_pod(namespace, pod)

    if pod_info is None:
        console.print("[red]Pod not found[/red]")
        raise typer.Exit()

    console.print(f"[green]Pod:[/green] {pod_info.metadata.name}")
    console.print(f"[green]Namespace:[/green] {pod_info.metadata.namespace}")
    console.print(f"[green]Status:[/green] {pod_info.status.phase}")
    console.print(f"[green]Node:[/green] {pod_info.spec.node_name}")

@app.command()
def logs(pod: str):
    """Show pod logs."""

    namespace = "kube-system"

    console.print(get_pod_logs(namespace, pod))
@app.command()
def hello():
    """Test command."""
    console.print("[cyan]Hello from Kubectl AI Plugin![/cyan]")


@app.command()
def pods():
    """List all Kubernetes pods."""

    table = Table(title="Kubernetes Pods")

    table.add_column("Namespace")
    table.add_column("Pod")
    table.add_column("Status")

    for pod in get_pods():
        table.add_row(
            pod.metadata.namespace,
            pod.metadata.name,
            pod.status.phase
        )

    console.print(table)


if __name__ == "__main__":
    app()