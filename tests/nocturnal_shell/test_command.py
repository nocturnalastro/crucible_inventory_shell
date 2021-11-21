from argparse import ArgumentParser
from unittest import mock

import pytest

from nocturnal_shell.command import Command
from nocturnal_shell.default_commands import Print


def test_command():
    arg_parser = ArgumentParser()

    class TheTestCommand(Command):
        name = "test_me"

    # TODO


@pytest.fixture
def mock_print():
    with mock.patch("nocturnal_shell.command.Command.output") as output:
        yield output


@pytest.fixture
def mock_shell():
    return None


def test_print(mock_print, mock_shell):
    print_cmd = Print()
    print_cmd.action(mock_shell, print_cmd.parse("hello world"))
    mock_print.assert_called_once_with("hello world")


def test_exit():
    # TODO
    pass


def test_help():
    # TODO
    pass
