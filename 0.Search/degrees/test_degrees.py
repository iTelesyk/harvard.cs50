import sys
import importlib
import pytest
import os


def test_main_small(monkeypatch):
    # Save original sys.argv
    original_argv = sys.argv.copy()
    sys.argv = ["degrees.py", "small"]
    # Import the module fresh to ensure main() runs
    importlib.reload(importlib.import_module("degrees"))
    # Restore sys.argv
    sys.argv = original_argv


def test_main_demi_to_tom(monkeypatch, capsys):
    # Simulate command-line argument for 'small' dataset
    original_argv = sys.argv.copy()
    sys.argv = ["degrees.py", "small"]
    # Change working directory to where the data is
    original_cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    # Simulate user input: 'Demi Moore' then 'Tom Cruise'
    inputs = iter(["Demi Moore", "Tom Cruise"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Import and call main_testable from degrees
    import degrees
    degrees.main_testable()
    # Capture output
    captured = capsys.readouterr()
    # Restore sys.argv and cwd
    sys.argv = original_argv
    os.chdir(original_cwd)
    # Check that output contains expected names
    assert "Demi Moore" in captured.out
    assert "Tom Cruise" in captured.out


