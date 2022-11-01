"""
Unit and regression test for the MDRDG package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import MDRDG


def test_MDRDG_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "MDRDG" in sys.modules
