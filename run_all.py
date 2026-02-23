#!/usr/bin/env python3
"""
Run all 25 comparison tests, or pick specific ones.
Output is saved to results/ automatically.

Usage:
  python run_all.py              # Run all 25 tests
  python run_all.py 1            # Run test 01 only
  python run_all.py 1 2 3        # Run tests 01, 02, 03
  python run_all.py 12-18        # Run tests 12 through 18
  python run_all.py --cleanup    # Delete all resources
  python run_all.py --list       # List all available tests
"""

import importlib
import io
import os
import sys
from datetime import datetime

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

ALL_TESTS = {
    1: ("Semantic Search (top-K cosine)", "test_01_semantic_search"),
    2: ("Filter: exact match", "test_02_filter_exact_match"),
    3: ("Filter: numeric range", "test_03_filter_numeric_range"),
    4: ("Filter: combined AND", "test_04_filter_combined_and"),
    5: ("Filter: OR logic", "test_05_filter_or"),
    6: ("Filter: negation", "test_06_filter_negation"),
    7: ("Filter: set membership", "test_07_filter_set_membership"),
    8: ("Insert batch", "test_08_insert_batch"),
    9: ("Get by ID", "test_09_get_by_id"),
    10: ("Update metadata", "test_10_update_metadata"),
    11: ("Delete vectors", "test_11_delete"),
    12: ("Hybrid search (Qdrant only)", "test_12_hybrid_search"),
    13: ("Recommendation (Qdrant only)", "test_13_recommendation"),
    14: ("Scroll/paginate (Qdrant only)", "test_14_scroll_paginate"),
    15: ("Full-text match (Qdrant only)", "test_15_fulltext_match"),
    16: ("Geo filtering (Qdrant only)", "test_16_geo_filter"),
    17: ("Grouping (Qdrant only)", "test_17_grouping"),
    18: ("Named vectors (Qdrant only)", "test_18_named_vectors"),
    19: ("Zero setup (S3 strength)", "test_19_zero_setup"),
    20: ("IAM auth (S3 strength)", "test_20_iam_auth"),
    21: ("Bedrock integration (S3 strength)", "test_21_bedrock_integration"),
    22: ("TopK limit", "test_22_topk_limit"),
    23: ("Consistency", "test_23_consistency"),
    24: ("Batch limits", "test_24_batch_limits"),
    25: ("Scale constraints", "test_25_scale_constraints"),
}


def parse_args(args: list[str]) -> list[int]:
    """Parse command line args into list of test numbers."""
    nums = []
    for a in args:
        if "-" in a and not a.startswith("-"):
            lo, hi = a.split("-", 1)
            nums.extend(range(int(lo), int(hi) + 1))
        else:
            nums.append(int(a))
    return sorted(set(nums))


class TeeWriter:
    """Write to both the real stdout and a StringIO buffer simultaneously."""

    def __init__(self, real_stdout, buffer):
        self.real_stdout = real_stdout
        self.buffer = buffer

    def write(self, text):
        self.real_stdout.write(text)
        self.buffer.write(text)

    def flush(self):
        self.real_stdout.flush()
        self.buffer.flush()


def save_output(test_num: int, module_name: str, content: str, status: str):
    """Save captured output to results/<test_module>.txt."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    filepath = os.path.join(RESULTS_DIR, f"{module_name}.txt")
    with open(filepath, "w") as f:
        f.write(f"# Test {test_num:02d} — {ALL_TESTS[test_num][0]}\n")
        f.write(f"# Status: {status}\n")
        f.write(f"# Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(content)
    return filepath


def main():
    args = sys.argv[1:]

    if "--cleanup" in args:
        from setup import cleanup_both

        cleanup_both()
        return

    if "--list" in args:
        print("Available tests:")
        for n, (name, _) in ALL_TESTS.items():
            cat = (
                "Common"
                if n <= 11
                else (
                    "Qdrant-Only"
                    if n <= 18
                    else ("S3-Strength" if n <= 21 else "Limits")
                )
            )
            print(f"  {n:>2}. [{cat}] {name}")
        return

    test_nums = parse_args(args) if args else list(ALL_TESTS.keys())

    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("╔══════════════════════════════════════════════════════╗")
    print("║     S3 Vectors vs Qdrant — 25 Comparison Tests      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"  Running {len(test_nums)} test(s): {test_nums}")
    print(f"  Results will be saved to: {RESULTS_DIR}/\n")

    passed, failed, saved_files = 0, 0, []

    for n in test_nums:
        if n not in ALL_TESTS:
            print(f"  ⚠ Test {n} does not exist, skipping.")
            continue

        name, module_name = ALL_TESTS[n]

        # Capture output while still printing to terminal
        buf = io.StringIO()
        tee = TeeWriter(sys.stdout, buf)
        old_stdout = sys.stdout

        try:
            sys.stdout = tee
            mod = importlib.import_module(f"tests.{module_name}")
            mod.run()
            sys.stdout = old_stdout
            status = "PASSED"
            passed += 1
        except Exception as e:
            sys.stdout = old_stdout
            print(f"\n  ✗ Test {n} ({name}) FAILED: {e}")
            buf.write(f"\n  ✗ FAILED: {e}\n")
            status = f"FAILED: {e}"
            failed += 1

        save_output(n, module_name, buf.getvalue(), status)
        saved_files.append((n, module_name, status))
        print()

    # Print summary
    print("=" * 60)
    print(f"  RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
    print(f"  Output saved to: {RESULTS_DIR}/")
    print("=" * 60)
    for n, mod, st in saved_files:
        icon = "✓" if "PASSED" in st else "✗"
        print(f"    {icon} Test {n:02d}: {mod}.txt")

    # Save a combined summary file
    summary_path = os.path.join(RESULTS_DIR, "_summary.txt")
    with open(summary_path, "w") as f:
        f.write("S3 Vectors vs Qdrant — Test Run Summary\n")
        f.write(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}\n\n")
        for n, mod, st in saved_files:
            icon = "✓" if "PASSED" in st else "✗"
            f.write(f"  {icon} Test {n:02d}: {ALL_TESTS[n][0]} — {st}\n")
        f.write(f"\nIndividual results in: {RESULTS_DIR}/\n")
    print(f"  Summary: {summary_path}")


if __name__ == "__main__":
    main()
    print("Done.")


if __name__ == "__main__":
    main()
