from nocturnal_shell.shell import Shell
from prompt_toolkit.formatted_text import HTML
from .entities.entities import CrucibleInventory


class CrucibleShellState:
    def __init__(self):
        self.inventory = CrucibleInventory()
        self.extras = {}


class CrucibleShell(Shell):
    def __init__(self, commands):
        self.state = CrucibleShellState()
        super().__init__(commands)

    def get_bottom_bar_html(self):
        if self.state.inventory.is_valid:
            return "<style bg='ansigreen'>Inventory is valid</style>"
        return "<style bg='ansired'>Inventory is not valid</style>"

    def get_prompt_args(self):
        prompt_args = super().get_prompt_args()
        prompt_args["bottom_toolbar"] = lambda: HTML(self.get_bottom_bar_html())
        return prompt_args
