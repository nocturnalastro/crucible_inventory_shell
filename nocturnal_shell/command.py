from abc import abstractmethod, ABC, abstractproperty
from argparse import ArgumentParser
from .exceptions import ActionException


class Command(ABC):
    requires_shell = False

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def arg_parser(self) -> ArgumentParser:
        pass

    @abstractmethod
    def action(self, state, args):
        pass

    def parse(self, arg_line):
        try:
            return self.arg_parser.parse_args(arg_line.split(" "))
        except SystemExit:
            raise ActionException from SystemExit

    @staticmethod
    def output(text):
        print(text)


class ShellBoundCommand(Command):
    requires_shell = True

    def __init__(self, shell) -> None:
        self._shell = shell
        super().__init__()
