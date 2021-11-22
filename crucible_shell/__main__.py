#!/usr/bin/env python

from .commands.add import AddNode, AddService
from .shell import CrucibleShell


if __name__ == "__main__":
    shell = CrucibleShell(
        commands=[
            AddNode,
            AddService,
        ]
    )
    shell.mainloop()
