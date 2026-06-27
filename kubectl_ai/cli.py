import typer
from rich.console import Console

app = typer.Typer(
    help="🤖 AI-powered kubectl plugin for Kubernetes troubleshooting."
)

console = Console()


@app.command()
def version():
    """Show plugin version."""
    console.print("[bold green]Kubectl AI Plugin[/bold green]")
    console.print("Version: 0.1.0")


@app.command()
def hello():
    """Test command."""
    console.print("[cyan]Hello from Kubectl AI Plugin![/cyan]")


if __name__ == "__main__":
    app()