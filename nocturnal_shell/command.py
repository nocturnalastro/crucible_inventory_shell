from abc import abstractmethod, ABC, abstractproperty
from argparse import ArgumentParser


class Command(ABC):
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
        return self.arg_parser.parse_args(arg_line.split(' '))
