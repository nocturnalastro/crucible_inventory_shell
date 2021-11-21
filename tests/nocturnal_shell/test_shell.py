import pytest
from unittest import mock
from collections import defaultdict
from nocturnal_shell.shell import Shell


@pytest.fixture
def patch_output():
    with mock.patch("nocturnal_shell.command.Command.output") as output:
        yield output


@pytest.fixture
def session():
    class DummySession:
        def __init__(self, responses) -> None:
            self.responses = responses
            self.counters = defaultdict(int)

        def prompt(self, prompt):
            index = self.counters[prompt]
            response = self.responses[prompt][index]
            self.counters[prompt] += 1
            return response


@pytest.fixture
def shell(session):
    class TestShell(Shell):
        def __init__(self):
            self.state = {}
            super().__init__(commands=[])

        def _init_session(self):
            self.session = session

    return TestShell()


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
