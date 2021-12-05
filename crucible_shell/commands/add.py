from nocturnal_shell.command import Command
from nocturnal_shell.exceptions import UserException

from crucible_inventory.services import AssistedInstaller, service_registry
from crucible_inventory.host import Node
from argparse import ArgumentParser


add_node_parser = ArgumentParser(prog="add_node", description="Add node to inventory")
add_node_parser.add_argument(
    "-i",
    "--host",
    type=str,
    required=True,
)
add_node_parser.add_argument(
    "-m",
    "--mac",
    type=str,
    required=True,
)
add_node_parser.add_argument(
    "-v",
    "--vendor",
    type=str,
    choices=Node.get_supported_vendors(),
    required=True,
)
add_node_parser.add_argument(
    "-n",
    "--name",
    type=str,
    required=True,
)
add_node_parser.add_argument(
    "-r",
    "--role",
    type=str,
    choices=Node.get_allowed_roles(),
    required=True,
)


class AddNode(Command):
    name = "add_node"
    arg_parser = add_node_parser

    @staticmethod
    def action(shell, args):
        node = Node(**vars(args))
        shell.state.inventory.add_node(node)


add_service_parser = ArgumentParser()
add_service_parser.add_argument("-i", "--host", type=str)

type_subparsers = add_service_parser.add_subparsers(dest="type")
assisted_installer_parser = type_subparsers.add_parser("AssistedInstaller")
assisted_installer_parser.add_argument("-n", "--hostname", type=str)


class AddService(Command):
    name = "add_service"
    arg_parser = add_service_parser

    @staticmethod
    def action(shell, args):
        try:
            ServiceClass = service_registry.entries[args.type]
        except KeyError:
            raise UserException(
                f"Type '{args.type}' not found in "
                f"'{ ','.join(service_registry.entries)}'"
            )

        service_args = ServiceClass.extract_vars(vars(args))
        shell.state.inventory.add_service(ServiceClass(**service_args))
