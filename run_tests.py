#!/usr/bin/env python3
"""
Test runner script for character-agent-integration.

Provides convenient ways to run tests with different options.
"""

import sys
import subprocess
from pathlib import Path


def run_tests(args=None):
    """Run pytest with the given arguments."""
    if args is None:
        args = []

    # Base pytest command
    cmd = ["python", "-m", "pytest"]

    # Add additional arguments
    cmd.extend(args)

    # Add test directory if not specified
    if not any(arg.startswith("tests/") or arg == "tests" for arg in args):
        cmd.append("tests/")

    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd)


def run_unit_tests():
    """Run only unit tests."""
    return run_tests(["-m", "unit", "-v"])


def run_integration_tests():
    """Run only integration tests."""
    return run_tests(["-m", "integration", "-v"])


def run_coverage():
    """Run tests with coverage report."""
    return run_tests([
        "--cov=character_agent_integration",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ])


def run_specific_test(test_file):
    """Run a specific test file."""
    return run_tests([f"tests/{test_file}", "-v"])


def run_fast_tests():
    """Run fast tests only (exclude slow)."""
    return run_tests(["-m", "not slow", "-v"])


def run_with_verbose_output():
    """Run tests with verbose output."""
    return run_tests(["-vv", "-s"])


def main():
    """Main entry point for test runner."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Test runner for character-agent-integration"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["all", "unit", "integration", "coverage", "fast", "verbose"],
        default="all",
        help="Test command to run"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Specific test file to run"
    )
    parser.add_argument(
        "--no-cov",
        action="store_true",
        help="Disable coverage reporting"
    )

    args = parser.parse_args()

    # If specific file is provided, run it
    if args.file:
        return run_specific_test(args.file)

    # Otherwise run based on command
    if args.no_cov:
        # Remove coverage from pytest.ini args
        import os
        os.environ["PYTEST_ADDOPTS"] = "-v --tb=short"

    if args.command == "all":
        return run_tests()
    elif args.command == "unit":
        return run_unit_tests()
    elif args.command == "integration":
        return run_integration_tests()
    elif args.command == "coverage":
        return run_coverage()
    elif args.command == "fast":
        return run_fast_tests()
    elif args.command == "verbose":
        return run_with_verbose_output()


if __name__ == "__main__":
    sys.exit(main().returncode)
