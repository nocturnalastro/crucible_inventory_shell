from crucible_shell.shell import Shell
import pytest


@pytest.fixture
def shell_class():
    return Shell
