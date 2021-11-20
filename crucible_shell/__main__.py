#!/usr/bin/env python
from nocturnal_shell.shell import Shell

from .entities.entities import CrucibleInventory


class CrucibleShellState:
    def __init__(self):
        self.inventory = CrucibleInventory()
        self.extras = {}


class CrucibleShell(Shell):
    def __init__(self, commands):
        self.state = CrucibleShellState()
        super().__init__(commands)
        print(self.state)


if __name__ == "__main__":
    shell = CrucibleShell(commands=[])
    shell.mainloop()
