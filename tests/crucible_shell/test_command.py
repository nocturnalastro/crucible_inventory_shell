from collections import defaultdict
from crucible_shell.commands.add import AddService, AddNode
from pytest import fixture
from crucible_shell.entities.entities import Node

from crucible_shell.entities.services import AssistedInstaller

@fixture
def mock_state():
    class Inventory:
        def __init__(self, state):
            self.state = state

        def add_service(self, service):
            self.state.store['service'].append(service)

        def add_node(self, node):
            self.state.store['node'].append(node)

    class State:
        def __init__(self):
            self.store = defaultdict(list)
            self.inventory = Inventory(self)

    return State()

@fixture
def host():
    return '10.4.0.100'

@fixture
def hostname():
    return 'ai.test.lab'

@fixture
def mac():
    return 'RETURN:OF:THE:MAC'

def test_add_assisted_installer(mock_state, host, hostname):
    cmd  = AddService()
    args = cmd.parse(f'-t AssistedInstaller -i {host} -n {hostname}')
    cmd.action(mock_state, args)
    result = mock_state.store['service'][0]
    assert isinstance(result, AssistedInstaller)
    assert result.host == host
    assert result.hostname == hostname
    assert result.port == 8090

def test_add_node(mock_state, host, hostname, mac):
    cmd  = AddNode()
    args = cmd.parse(f'-i {host} -n {hostname} -m {mac} -v KVM -r master')
    cmd.action(mock_state, args)
    result = mock_state.store['node'][0]
    assert isinstance(result, Node)
    assert result.host == host
    assert result.name == hostname
