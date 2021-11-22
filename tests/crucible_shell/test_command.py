from collections import defaultdict
from crucible_shell.commands.add import AddService, AddNode
from crucible_shell.entities.entities import Node
import pytest
from crucible_shell.entities.services import AssistedInstaller
from crucible_shell.shell import Shell


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
    args = cmd.parse(f"-t AssistedInstaller -i {host} -n {hostname}")
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
