#!/usr/bin/env python3
"""
S3 Vectors vs Qdrant — Side-by-Side Comparison
Run: python run.py [--round 1|2|3|4|5] [--cleanup]
"""

import argparse
import sys

from clients.qdrant_ops import QdrantOps
from clients.s3vectors_ops import S3VectorsOps
from rich.console import Console

from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME
from core.dataset import MOVIES
from core.display import console
from core.embeddings import generate_movie_embeddings


def setup(qdrant: QdrantOps, s3v: S3VectorsOps) -> dict:
    """Setup both platforms and insert movies. Returns embeddings dict."""
    console.rule("[bold]Setup: Preparing both platforms[/]")

    # Generate embeddings (cached)
    console.print("\n[bold]Step 1:[/] Generating embeddings...")
    embeddings = generate_movie_embeddings(MOVIES)

    # Setup Qdrant
    console.print("\n[bold]Step 2:[/] Setting up Qdrant...")
    qdrant.create_collection()
    qdrant.insert_movies(MOVIES, embeddings)
    info = qdrant.collection_info()
    console.print(
        f"  Qdrant: {info['points_count']} vectors loaded, status={info['status']}"
    )

    # Setup S3 Vectors
    console.print("\n[bold]Step 3:[/] Setting up S3 Vectors...")
    s3v.create_bucket_and_index()
    s3v.insert_movies(MOVIES, embeddings)
    count = s3v.count()
    console.print(f"  S3 Vectors: {count} vectors loaded")

    console.print("\n[green]✓ Both platforms ready with {len(MOVIES)} movies.[/]\n")
    return embeddings


def cleanup(qdrant: QdrantOps, s3v: S3VectorsOps):
    """Delete all resources on both platforms."""
    console.rule("[bold red]Cleanup[/]")
    console.print("  Deleting Qdrant collection...")
    qdrant.cleanup()
    console.print("  Deleting S3 Vectors bucket & index...")
    s3v.cleanup()
    console.print("[green]✓ All resources cleaned up.[/]")


def main():
    parser = argparse.ArgumentParser(description="S3 Vectors vs Qdrant Comparison")
    parser.add_argument(
        "--round",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=None,
        help="Run a specific round (1-5). Default: run all.",
    )
    parser.add_argument(
        "--cleanup", action="store_true", help="Delete all resources after running."
    )
    parser.add_argument(
        "--cleanup-only",
        action="store_true",
        help="Only cleanup — don't run any tests.",
    )
    args = parser.parse_args()

    qdrant = QdrantOps()
    s3v = S3VectorsOps()

    if args.cleanup_only:
        cleanup(qdrant, s3v)
        return

    # --- Banner ---
    console.print()
    console.print(
        "[bold magenta]╔══════════════════════════════════════════════════╗[/]"
    )
    console.print(
        "[bold magenta]║     S3 Vectors vs Qdrant — Movie Search Test    ║[/]"
    )
    console.print(
        "[bold magenta]╚══════════════════════════════════════════════════╝[/]"
    )
    console.print()

    # --- Setup ---
    embeddings = setup(qdrant, s3v)

    # --- Import rounds ---
    from rounds import (
        round1_common,
        round2_qdrant_only,
        round3_s3_strengths,
        round4_limits,
        round5_verdict,
    )

    rounds = {
        1: lambda: round1_common.run(qdrant, s3v),
        2: lambda: round2_qdrant_only.run(qdrant),
        3: lambda: round3_s3_strengths.run(),
        4: lambda: round4_limits.run(qdrant, s3v, embeddings),
        5: lambda: round5_verdict.run(),
    }

    if args.round:
        rounds[args.round]()
    else:
        for r in [1, 2, 3, 4, 5]:
            rounds[r]()

    # --- Cleanup ---
    if args.cleanup:
        cleanup(qdrant, s3v)

    console.print("\n[bold green]Done![/]\n")


if __name__ == "__main__":
    main()
