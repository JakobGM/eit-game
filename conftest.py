import pytest

@pytest.fixture(autouse=True)
def set_logging_level(caplog):
    """Print debug logs."""
    caplog.set_level(logging.DEBUG)
