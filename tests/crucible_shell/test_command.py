import pytest
from crucible_inventory.host import Node
from crucible_inventory.services import AssistedInstaller

from crucible_shell.commands.add import AddNode, AddService


@pytest.fixture
def host():
    return "10.4.0.100"


@pytest.fixture
def hostname():
    return "ai.test.lab"


@pytest.fixture
def mac():
    return "RETURN:OF:THE:MAC"


def test_add_assisted_installer(shell, state, host, hostname):
    cmd = AddService()
    args = cmd.parse(f"AssistedInstaller -i {host} -n {hostname}")
    cmd.action(shell, args)
    result = state.store["service"][0]
    assert isinstance(result, AssistedInstaller)
    assert result.host == host
    assert result.hostname == hostname
    assert result.port == 8090


def test_add_node(shell, state, host, hostname, mac):
    cmd = AddNode()
    args = cmd.parse(f"-i {host} -n {hostname} -m {mac} -v KVM -r master")
    cmd.action(shell, args)
    result = state.store["node"][0]
    assert isinstance(result, Node)
    assert result.host == host
    assert result.name == hostname
