from .command import Command
from argparse import ArgumentParser


class Help(Command):
    name = "help"
    arg_parser = None
    requires_shell = True

    def get_command_list(self, shell):
        return [cmd_name for cmd_name in shell.commands.keys()]

    def parse(self, arg_line):
        return {}

    def action(self, shell, _args):
        self.output(f"Help: {self.get_command_list(shell)}")
        return None


class CommandNotFound(Help):
    name = "_NOT_FOUND"
    arg_parser = None

    def parse(self, action_name):
        return action_name

    def action(self, shell, action_name):
        self.output(
            " ".join(
                [
                    f"Command ('{action_name}') not found!",
                    "Valid commands are:",
                    f"{self.get_command_list(shell)}",
                ]
            )
        )


class NoInput(Command):
    name = None
    arg_parser = None

    def parse(self, arg_line):
        return {}

    @staticmethod
    def action(_shell, _args):
        return None


class Exit(Command):
    name = "exit"
    arg_parser = None

    def parse(self, arg_line):
        return {}

    @staticmethod
    def action(shell, _args):
        shell.exit()
        return None


print_parser = ArgumentParser()
print_parser.add_argument("text", type=str, nargs="+", help="text to print out")


class Print(Command):
    name = "print"
    arg_parser = print_parser

    def action(self, _shell, args):
        self.output(" ".join(args.text))
        return None
