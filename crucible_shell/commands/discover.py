from nocturnal_shell.command import Command
from argparse import ArgumentParser

discover_args_parser = ArgumentParser(description="")


class AutoDiscovery(Command):
    name = "discover"
    arg_parser = discover_args_parser

    def action(self, shell, args):
        pass
