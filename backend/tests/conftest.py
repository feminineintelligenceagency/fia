import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests that call OpenAI (deselect with '-m \"not slow\"')")
