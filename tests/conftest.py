import pytest
from collections import defaultdict
from unittest import mock


@pytest.fixture
def state():
    class Inventory:
        def __init__(self, state):
            self.state = state

        def add_service(self, service):
            self.state.store["service"].append(service)

        def add_node(self, node):
            self.state.store["node"].append(node)

    class State:
        def __init__(self):
            self.store = defaultdict(list)
            self.inventory = Inventory(self)

    return State()


@pytest.fixture
def responses():
    return {}


@pytest.fixture
def commands():
    return []


@pytest.fixture
def session(responses):
    class DummySession:
        def __init__(self, responses) -> None:
            self.responses = responses
            self.counters = defaultdict(int)

        def prompt(self, prompt):
            index = self.counters[prompt]
            response = self.responses[prompt][index]
            self.counters[prompt] += 1
            return response

    return DummySession(responses)


@pytest.fixture
def shell(shell_class, session, state, commands):
    class TestShell(shell_class):
        def __init__(self):
            self.state = state
            super().__init__(commands=commands)

        def _init_session(self):
            self.session = session

    return TestShell()


@pytest.fixture
def patch_output():
    with mock.patch("nocturnal_shell.command.Command.output") as output:
        yield output
