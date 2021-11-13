from nocturnal_shell.command import Command  #
from ..entities.services import service_registry
from ..entities.entities import Node
from argparse import ArgumentParser

add_node_parser = ArgumentParser()

add_node_parser = ArgumentParser()
add_node_parser.add_argument(
    '-i', '--host', type=str
)
add_node_parser.add_argument(
    '-m', '--mac', type=str
)
add_node_parser.add_argument(
    '-v', '--vendor', type=str, choices=Node.SUPPORTED_VENDORS
)
add_node_parser.add_argument(
    '-n', '--name', type=str
)
add_node_parser.add_argument(
    '-r', '--role', type=str, choices=Node.ALLOWED_ROLES
)


class AddNode(Command):
    name = "add_node"
    arg_parser = add_node_parser

    @staticmethod
    def action(state, args):
        state.inventory.add_node(Node(**vars(args)))


add_service_parser = ArgumentParser()
add_service_parser.add_argument(
    '-t', '--type', choices=service_registry.entries,
)
add_service_parser.add_argument(
    '-i', '--host', type=str
)
add_service_parser.add_argument(
    '-n', '--hostname', type=str
)

class AddService(Command):
    name = "add_service"
    arg_parser = add_service_parser

    @staticmethod
    def action(state, args):
        ServiceClass = service_registry.entries[args.type]
        service_args = dict(**vars(args))
        service_args.pop('type') # Remove type as to not interfere with Service
        state.inventory.add_service(ServiceClass(**service_args))

