#!/bin/bash

# ============================================================================
# Test Runner for User Account Management System
# ============================================================================

echo "================================================================================"
echo "Running tests for User Account Management System"
echo "================================================================================"

# Run the tests using unittest discover
python3 -m unittest discover -s tests -p "test_*.py" -v

# Store the exit code
EXIT_CODE=$?

echo "================================================================================"
echo "Test execution complete"
echo "================================================================================"

# Return the exit code from unittest
exit $EXIT_CODE
