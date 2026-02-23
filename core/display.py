"""Rich display helpers for comparison output."""

import time
from contextlib import contextmanager

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


@contextmanager
def timer(label: str = ""):
    """Context manager that yields elapsed ms."""
    result = {"ms": 0.0}
    start = time.perf_counter()
    try:
        yield result
    finally:
        result["ms"] = (time.perf_counter() - start) * 1000


def round_header(round_num: int, title: str, subtitle: str = ""):
    """Print a styled round header."""
    console.print()
    console.rule(f"[bold cyan]ROUND {round_num}: {title}[/]", style="cyan")
    if subtitle:
        console.print(f"  [dim]{subtitle}[/]")
    console.print()


def test_header(test_id: str, name: str):
    """Print a test sub-header."""
    console.print(f"  [bold yellow]▶ {test_id}: {name}[/]")


def results_table(
    query: str,
    qdrant_results: list[dict] | None,
    s3v_results: list[dict] | None,
    qdrant_ms: float = 0,
    s3v_ms: float = 0,
):
    """Side-by-side search results table."""
    table = Table(title=f'"{query}"', show_header=True, header_style="bold")
    table.add_column("#", width=3)
    table.add_column(f"Qdrant ({qdrant_ms:.0f}ms)", ratio=1)
    table.add_column("Score", width=6)
    table.add_column(f"S3 Vectors ({s3v_ms:.0f}ms)", ratio=1)
    table.add_column("Score", width=6)

    max_rows = max(
        len(qdrant_results) if qdrant_results else 0,
        len(s3v_results) if s3v_results else 0,
    )
    for i in range(max_rows):
        q_title = (
            qdrant_results[i]["title"]
            if qdrant_results and i < len(qdrant_results)
            else "—"
        )
        q_score = (
            f"{qdrant_results[i]['score']:.3f}"
            if qdrant_results and i < len(qdrant_results)
            else "—"
        )
        s_title = (
            s3v_results[i]["title"] if s3v_results and i < len(s3v_results) else "—"
        )
        s_score = (
            f"{s3v_results[i]['score']:.3f}"
            if s3v_results and i < len(s3v_results)
            else "—"
        )
        table.add_row(str(i + 1), q_title, q_score, s_title, s_score)

    console.print(table)
    console.print()


def single_results_table(platform: str, results: list[dict], ms: float = 0):
    """Results table for a single platform."""
    table = Table(title=f"{platform} ({ms:.0f}ms)", show_header=True)
    table.add_column("#", width=3)
    table.add_column("Title", ratio=2)
    table.add_column("Score", width=8)
    table.add_column("Genre", width=12)
    table.add_column("Year", width=6)
    table.add_column("Rating", width=6)

    for i, r in enumerate(results):
        table.add_row(
            str(i + 1),
            r.get("title", "?"),
            f"{r.get('score', 0):.3f}",
            r.get("genre", "?"),
            str(r.get("year", "?")),
            str(r.get("rating", "?")),
        )
    console.print(table)
    console.print()


def feature_row(feature: str, qdrant: str, s3v: str):
    """Returns a tuple for feature comparison."""
    return (feature, qdrant, s3v)


def print_feature_table(rows: list[tuple], title: str = "Feature Comparison"):
    """Print a feature comparison table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Feature", ratio=2)
    table.add_column("Qdrant", justify="center", width=12)
    table.add_column("S3 Vectors", justify="center", width=12)
    for row in rows:
        table.add_row(*row)
    console.print(table)
    console.print()


def success(msg: str):
    console.print(f"    [green]✓[/] {msg}")


def fail(msg: str):
    console.print(f"    [red]✗[/] {msg}")


def info(msg: str):
    console.print(f"    [dim]ℹ {msg}[/]")


def not_supported(platform: str, feature: str):
    console.print(f"    [red]✗ {platform}:[/] {feature} — [dim]Not supported[/]")
