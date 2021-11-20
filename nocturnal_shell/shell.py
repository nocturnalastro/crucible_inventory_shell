from prompt_toolkit import PromptSession

from . import default_commands as cmds
from .command import Command
from .logging import rootLogger
from .exceptions import NoState, ActionException


class Shell:
    NONE = cmds.NoInput()
    NOT_FOUND_CLASS = cmds.CommandNotFound
    DEFAULT_COMMANDS = [
        cmds.Exit,
        cmds.Help,
        cmds.Print,
    ]
    DEFAULT_PROMPT = "$> "
    LOGGER = rootLogger

    def __init__(self, commands):
        self._exit = False
        self.NOT_FOUND = self._init_cmd(cmds.CommandNotFound)
        self.commands = {
            c.name: c for c in map(self._init_cmd, (commands + self.DEFAULT_COMMANDS))
        }
        self.session = PromptSession()
        if not hasattr(self, "state"):
            raise NoState()

    def _init_cmd(self, cmd):
        return cmd(self) if cmd.requires_shell else cmd()

    @property
    def prompt_text(self):
        return self.DEFAULT_PROMPT

    def exit(self):
        self._exit = True

    @property
    def end_loop(self):
        return self._exit

    def mainloop(self):
        while not self.end_loop:
            try:
                self.handle(self.session.prompt(self.prompt_text))
            except ActionException as err:
                self.LOGGER.debug(err)
                continue
            except Exception as err:
                self.LOGGER.error(err)
                continue

    def process_response(self, response) -> tuple[Command, str]:
        action_name, *args = response.split(" ", 1)
        if action_name == "":
            return self.NONE, ""
        try:
            return self.commands[action_name], (args[0] if args else "")
        except KeyError:
            return self.NOT_FOUND, action_name

    def handle(self, response):
        command, args = self.process_response(response)
        command.action(self.state, command.parse(args))
