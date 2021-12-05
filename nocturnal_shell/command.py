from abc import abstractmethod, ABC, abstractproperty
from argparse import ArgumentParser, Namespace
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

    @property
    def _argparse_defaults(self):
        defaults = {}
        for a in self.arg_parser._actions:
            defaults[a.dest] = a.default
        return defaults

    def merge_namespaces(self, *namespaces):
        # Merge a top layer of namespaces
        values = vars(namespaces[0])
        defaults = self._argparse_defaults
        for namespace in namespaces[1:]:
            for name, value in vars(namespace).items():
                if value != defaults[name]:
                    values[name] = value
        return Namespace(**values)

    def parse(self, arg_line):
        args, unparsed = self.arg_parser.parse_known_args(arg_line.split(" "))
        # This is to allow global arguments to be after subparser arguments
        if unparsed:
            re_parsed, still_unknown = self.arg_parser.parse_known_args(unparsed)
            args = self.merge_namespaces(args, re_parsed)
            if still_unknown:
                raise ActionException("unrecognized arguments {still_unknown}")
        return args

    @staticmethod
    def output(text):
        print(text)
