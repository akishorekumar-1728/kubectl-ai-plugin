import typer
from rich.console import Console
from rich.table import Table

from kubectl_ai.prompts import deployment_prompt
from kubectl_ai.kubernetes import get_deployment, get_events

from kubectl_ai.kubernetes import get_all_pods
from kubectl_ai.prompts import cluster_prompt

from kubectl_ai.ai import ask_ai
from kubectl_ai.prompts import pod_failure_prompt
from kubectl_ai.kubernetes import (
    get_pods,
    get_pod,
    get_pod_logs,
    get_pod_status,
)

app = typer.Typer(
    help="🤖 AI-powered kubectl plugin for Kubernetes troubleshooting."
)

console = Console()

@app.command("explain-deployment")
def explain_deployment(name: str, namespace: str = "default"):
    """Explain Kubernetes deployment issues using AI."""

    try:
        deployment = get_deployment(namespace, name)
        events = get_events(namespace)

        prompt = deployment_prompt(deployment, events.items)

        console.print("[yellow]Analyzing deployment with AI...[/yellow]")

        answer = ask_ai(prompt)
        console.print(answer)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit()

# ----------------------------
# AI ASK COMMAND
# ----------------------------
@app.command()
def ask(question: str):
    """Ask AI about Kubernetes."""
    console.print("[bold green]Thinking...[/bold green]")
    answer = ask_ai(question)
    console.print(answer)


# ----------------------------
# WHY POD FAILED (AI DEBUGGER)
# ----------------------------
@app.command("why-pod-failed")
def why_pod_failed(pod: str, namespace: str = "default"):
    """Analyze why a pod failed using AI."""

    try:
        status = get_pod_status(namespace, pod)
        logs = get_pod_logs(namespace, pod)

        prompt = pod_failure_prompt(status, logs)

        console.print("[yellow]Analyzing with AI...[/yellow]")

        answer = ask_ai(prompt)
        console.print(answer)

    except Exception as e:
        console.print(f"[red]Kubernetes Error:[/red] {str(e)}")
        raise typer.Exit()

@app.command("analyze-cluster")
def analyze_cluster():
    """Analyze entire Kubernetes cluster health using AI."""

    try:
        pods = get_all_pods()

        pod_summary = []

        for p in pods:
            pod_summary.append({
                "name": p.metadata.name,
                "namespace": p.metadata.namespace,
                "status": p.status.phase
            })

        prompt = cluster_prompt(pod_summary)

        console.print("[yellow]Analyzing cluster health with AI...[/yellow]")

        answer = ask_ai(prompt)
        console.print(answer)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit()
# ----------------------------
# VERSION
# ----------------------------
@app.command()
def version():
    """Show plugin version."""
    console.print("[bold green]Kubectl AI Plugin[/bold green]")
    console.print("Version: 0.1.0")


# ----------------------------
# DESCRIBE POD
# ----------------------------
@app.command()
def describe(pod: str, namespace: str = "kube-system"):
    """Describe a pod."""

    try:
        pod_info = get_pod(namespace, pod)

        if pod_info is None:
            console.print("[red]Pod not found[/red]")
            raise typer.Exit()

        console.print(f"[green]Pod:[/green] {pod_info.metadata.name}")
        console.print(f"[green]Namespace:[/green] {pod_info.metadata.namespace}")
        console.print(f"[green]Status:[/green] {pod_info.status.phase}")
        console.print(f"[green]Node:[/green] {pod_info.spec.node_name}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit()


# ----------------------------
# LOGS COMMAND
# ----------------------------
@app.command()
def logs(pod: str, namespace: str = "kube-system"):
    """Show pod logs."""

    try:
        console.print(get_pod_logs(namespace, pod))
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit()


# ----------------------------
# HELLO
# ----------------------------
@app.command()
def hello():
    """Test command."""
    console.print("[cyan]Hello from Kubectl AI Plugin![/cyan]")


# ----------------------------
# POD LIST
# ----------------------------
@app.command()
def pods(namespace: str = "kube-system"):
    """List pods in a namespace."""

    table = Table(title=f"Kubernetes Pods ({namespace})")

    table.add_column("Namespace")
    table.add_column("Pod")
    table.add_column("Status")

    try:
        for pod in get_pods():
            if pod.metadata.namespace == namespace:
                table.add_row(
                    pod.metadata.namespace,
                    pod.metadata.name,
                    pod.status.phase,
                )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit()


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    app()