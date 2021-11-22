from abc import abstractmethod, ABC, abstractproperty
from argparse import ArgumentParser
from .exceptions import ActionException


class Command(ABC):
    """Commands are the functionality of the shell
    They required an arg_parser with a parse_args method and an action function.
    The action method will recive
    """

    requires_shell = False

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def arg_parser(self) -> ArgumentParser:
        pass

    @abstractmethod
    def action(self, shell, args):
        pass

    def parse(self, arg_line):
        try:
            return self.arg_parser.parse_args(arg_line.split(" "))
        except SystemExit:
            raise ActionException from SystemExit

    @staticmethod
    def output(text):
        print(text)
