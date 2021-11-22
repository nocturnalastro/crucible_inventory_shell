import pytest
from unittest import mock
from collections import defaultdict
from nocturnal_shell.shell import Shell


@pytest.mark.parametrize(
    "command, expected_result",
    [
        pytest.param(
            "NOT_A_COMMAND",
            (
                "Command ('NOT_A_COMMAND') not found! "
                "Valid commands are: ['exit', 'help', 'print']"
            ),
        ),
        pytest.param("print hello world", "hello world"),
    ],
)
def test_commands(shell, patch_output, command, expected_result):
    shell.handle(command)
    patch_output.assert_called_once_with(expected_result)


def test_exit(shell):
    shell.handle("exit")
    assert shell.continue_loop is False
