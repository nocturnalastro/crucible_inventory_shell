from prompt_toolkit.completion import Completer, WordCompleter, NestedCompleter
from prompt_toolkit.document import Document
from argparse import (
    _SubParsersAction as SubParsersAction,
    _StoreAction as StoreAction,
)


class Skip:
    pass


SKIP_ME = Skip()


class CommandCompleter(Completer):
    @staticmethod
    def _parse_action(action):
        name = action.option_strings[-1]

        if action.nargs == 0:
            value = None
        elif action.choices:
            value = set(action.choices)
        else:
            value = SKIP_ME

        return (name, value)

    def _get_layers(self, argparser):
        if argparser is None:
            return None
        try:
            layer = {}

            for a in argparser._actions:
                if isinstance(a, StoreAction):
                    name, value = self._parse_action(a)
                    layer[name] = value
                elif isinstance(a, SubParsersAction):
                    for name, choice in a.choices.items():
                        layer[name] = self._get_layers(choice)
                else:
                    continue

            return layer
        except Exception as _err:
            return None

    def __init__(self, commands):

        self.options = self._get_options(
            {
                name: (
                    self._get_layers(cmd.arg_parser)
                    if hasattr(cmd, "arg_parser")
                    else cmd
                )
                for name, cmd in commands.items()
            }
        )
        self.ignore_case = True

    def _get_options(self, data):
        options = {}
        for key, value in data.items():
            if isinstance(value, Completer):
                options[key] = value
            elif isinstance(value, dict):
                options[key] = type(self)(value)
            elif isinstance(value, set):
                options[key] = type(self)({item: None for item in value})
            elif isinstance(value, Skip):
                options[key] = SKIP_ME
            else:
                assert value is None
                options[key] = None

        return options

    def get_completions(self, document, complete_event, check_first=True):
        # Split document.
        text = document.text_before_cursor.lstrip()
        stripped_len = len(document.text_before_cursor) - len(text)

        # If there is a space, check for the first term, and use a
        # subcompleter.
        handled = False

        if " " in text:
            if check_first:
                term = text.split()[0]
            else:
                term = text.split()[-1]

            completer = self.options.get(term)

            if completer is SKIP_ME:
                return

            # If we have a sub completer, use this for the completions.
            if completer is not None:
                handled = True
                if len(completer.options):
                    if check_first:
                        remaining_text = text[len(term) :].lstrip()
                    else:
                        remaining_text = text[-len(term) :].lstrip()
                    move_cursor = len(text) - len(remaining_text) + stripped_len

                    new_document = Document(
                        remaining_text,
                        cursor_position=document.cursor_position - move_cursor,
                    )

                    if isinstance(completer, CommandCompleter):
                        completions = completer.get_completions(
                            new_document, complete_event, check_first=False
                        )
                    else:
                        completions = completer.get_completions(
                            new_document, complete_event
                        )

                    for c in completions:
                        yield c

        if not handled:
            completer = WordCompleter(
                list(self.options.keys()), ignore_case=self.ignore_case
            )
            for c in completer.get_completions(document, complete_event):
                yield c
