from .command import Command
from prompt_toolkit import PromptSession

class CommandNotFound(Command):
    name = None
    arg_parser = None

    def parse(self, arg_line):
        return {}

    @staticmethod
    def action(_shell, **_args):
        print("Command not found! Valid commands are: ")


class Shell:

    NOT_FOUND = CommandNotFound()

    def __init__(self, commands):
        self._exit = False
        self._commands = {c.name: c for c in commands}
        self.session = PromptSession()

    @property
    def prompt_text(self):
        return "$>"

    @property
    def end_loop(self):
        return not self._exit

    def mainloop(self):
        while not self.end_loop:
            self.handle(self.session.prompt(self.prompt_text))

    def process_response(self, response):
        # TODO something more interesting perhaps using argparser
        action_name, args = response.split(" ", 1)
        try:
            return self._commands[action_name], args
        except KeyError:
            return self.NOT_FOUND, []

    def handle(self, response):
        command, args = self.process_response(response)
        command.action(self.state, command.parse(args))
