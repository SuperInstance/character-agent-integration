#!/usr/bin/env python3
"""
Verification script for test suite.
Checks that all test files are present and valid.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} NOT FOUND: {filepath}")
        return False

def check_file_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"  ✓ Valid syntax")
        return True
    except SyntaxError as e:
        print(f"  ✗ Syntax error: {e}")
        return False

def main():
    """Main verification function."""
    print("=" * 70)
    print("VERIFICATION: Character-Agent Integration Test Suite")
    print("=" * 70)
    print()

    checks_passed = 0
    checks_total = 0

    # Check test files
    print("1. TEST FILES")
    print("-" * 70)
    test_files = [
        ("tests/__init__.py", "Test package init"),
        ("tests/conftest.py", "Pytest fixtures"),
        ("tests/test_agent_roles.py", "Agent roles tests"),
        ("tests/test_memory_decisions.py", "Memory decisions tests"),
        ("tests/test_personality_learning.py", "Personality learning tests"),
        ("tests/test_emotion_intelligence.py", "Emotional intelligence tests"),
        ("tests/test_integration.py", "Integration tests"),
    ]

    for filepath, description in test_files:
        checks_total += 1
        if check_file_exists(filepath, description):
            if filepath.endswith('.py'):
                if check_file_syntax(filepath):
                    checks_passed += 1
        else:
            print()

    # Check configuration files
    print("\n2. CONFIGURATION FILES")
    print("-" * 70)
    config_files = [
        ("pytest.ini", "Pytest configuration"),
        (".coveragerc", "Coverage configuration"),
        ("run_tests.py", "Python test runner"),
        ("tests/run_tests.sh", "Bash test runner"),
    ]

    for filepath, description in config_files:
        checks_total += 1
        if check_file_exists(filepath, description):
            checks_passed += 1
        print()

    # Check documentation
    print("\n3. DOCUMENTATION")
    print("-" * 70)
    doc_files = [
        ("tests/README.md", "Test documentation"),
        ("tests/TEST_SUMMARY.md", "Test summary"),
    ]

    for filepath, description in doc_files:
        checks_total += 1
        if check_file_exists(filepath, description):
            checks_passed += 1
        print()

    # Count test cases
    print("\n4. TEST STATISTICS")
    print("-" * 70)
    total_lines = 0
    test_count = 0

    for filepath in ["tests/test_agent_roles.py", "tests/test_memory_decisions.py",
                     "tests/test_personality_learning.py", "tests/test_emotion_intelligence.py",
                     "tests/test_integration.py"]:
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                lines = len(f.readlines())
                total_lines += lines
                # Count test functions (approximate)
                f.seek(0)
                test_count += sum(1 for line in f if line.strip().startswith('def test_'))

    print(f"✓ Total test code lines: {total_lines}")
    print(f"✓ Approximate test cases: {test_count}")
    print()

    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"Checks passed: {checks_passed}/{checks_total}")
    print(f"Success rate: {100 * checks_passed / checks_total:.1f}%")
    print()

    if checks_passed == checks_total:
        print("✓ ALL CHECKS PASSED!")
        print("\nThe test suite is ready to use.")
        print("\nQuick start:")
        print("  pytest                    # Run all tests")
        print("  python run_tests.py       # Run with Python script")
        print("  ./tests/run_tests.sh      # Run with bash script")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("\nPlease review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
