#!/usr/bin/env python3
"""
Run all 25 S3 Vectors vs Qdrant comparison tests.
Captures every test's output and writes it to a single report file.

Usage:
    python run_all.py
"""

import importlib
import io
import sys
from datetime import datetime
from pathlib import Path

REPORT_PATH = Path(__file__).parent / "report.txt"

TESTS = [
    (1, "test_01_semantic_search"),
    (2, "test_02_filter_exact_match"),
    (3, "test_03_filter_numeric_range"),
    (4, "test_04_filter_combined_and"),
    (5, "test_05_filter_or"),
    (6, "test_06_filter_negation"),
    (7, "test_07_filter_set_membership"),
    (8, "test_08_insert_batch"),
    (9, "test_09_get_by_id"),
    (10, "test_10_update_metadata"),
    (11, "test_11_delete"),
    (12, "test_12_hybrid_search"),
    (13, "test_13_recommendation"),
    (14, "test_14_scroll_paginate"),
    (15, "test_15_fulltext_match"),
    (16, "test_16_geo_filter"),
    (17, "test_17_grouping"),
    (18, "test_18_named_vectors"),
    (19, "test_19_zero_setup"),
    (20, "test_20_iam_auth"),
    (21, "test_21_bedrock_integration"),
    (22, "test_22_topk_limit"),
    (23, "test_23_consistency"),
    (24, "test_24_batch_limits"),
    (25, "test_25_scale_constraints"),
]


def capture_test_output(module_name: str) -> tuple[str, bool]:
    """Run a test module and return (captured_output, success)."""
    buf = io.StringIO()
    original_stdout = sys.stdout

    try:
        sys.stdout = buf
        mod = importlib.import_module(f"tests.{module_name}")
        mod.run()
        return buf.getvalue(), True
    except Exception as e:
        return f"{buf.getvalue()}\n  ERROR: {e}\n", False
    finally:
        sys.stdout = original_stdout


def build_report(results: list[tuple[int, str, str, bool]]) -> str:
    """Build the full report string from all test results."""
    lines = [
        "S3 Vectors vs Qdrant — Full Test Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
    ]

    passed = sum(1 for *_, ok in results if ok)
    total = len(results)
    lines.append(f"Total: {total} | Passed: {passed} | Failed: {total - passed}")
    lines.append("")

    for num, name, output, success in results:
        status = "PASSED" if success else "FAILED"
        lines.append(f"{'─' * 60}")
        lines.append(f"TEST {num:02d} [{status}] — {name}")
        lines.append(f"{'─' * 60}")
        lines.append(output.strip())
        lines.append("")

    return "\n".join(lines)


def main():
    print("Running all 25 tests...\n")

    results = []
    for num, module_name in TESTS:
        print(f"  [{num:02d}/25] {module_name}...", end=" ", flush=True)
        output, success = capture_test_output(module_name)
        icon = "✓" if success else "✗"
        print(icon)
        results.append((num, module_name, output, success))

    report = build_report(results)
    REPORT_PATH.write_text(report)

    passed = sum(1 for *_, ok in results if ok)
    failed = len(results) - passed
    print(f"\nDone. {passed} passed, {failed} failed.")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
