from .command import Command, ShellBoundCommand
from argparse import ArgumentParser


class Help(ShellBoundCommand):
    name = "help"
    arg_parser = None
    requires_shell = True

    @property
    def command_list(self):
        return [cmd_name for cmd_name in self._shell.commands.keys()]

    def parse(self, arg_line):
        return {}

    def action(self, _state, _args):
        self.output(f"Help: {self.command_list}")
        return None


class CommandNotFound(Help):
    name = "_NOT_FOUND"
    arg_parser = None

    def parse(self, action_name):
        return action_name

    def action(self, _state, action_name):
        self.output(
            " ".join(
                [
                    f"Command ('{action_name}') not found!",
                    "Valid commands are:",
                    f"{self.command_list}",
                ]
            )
        )


class NoInput(Command):
    name = None
    arg_parser = None

    def parse(self, arg_line):
        return {}

    @staticmethod
    def action(_state, _args):
        return None


class Exit(ShellBoundCommand):
    name = "exit"
    arg_parser = None
    requires_shell = True

    def parse(self, arg_line):
        return {}

    def action(self, _state, _args):
        self._shell.exit()
        return None


class Help(ShellBoundCommand):
    name = "help"
    arg_parser = None
    requires_shell = True

    @property
    def command_list(self):
        return [cmd_name for cmd_name in self._shell.commands.keys()]

    def parse(self, arg_line):
        return {}

    def action(self, _state, _args):
        self.output(f"Help: {self.command_list}")
        return None


print_parser = ArgumentParser()
print_parser.add_argument("text", type=str, nargs="+", help="text to print out")


class Print(Command):
    name = "print"
    arg_parser = print_parser

    def action(self, _state, args):
        self.output(f"{''.join(args.text)}")
        return None
