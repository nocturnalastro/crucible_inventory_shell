from nocturnal_shell.command import Command
from argparse import ArgumentParser


def test_command():
    arg_parser = ArgumentParser()

    class TheTestCommand(Command):
        name = "test_me"
        